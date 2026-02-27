from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app import models
from app.auth import (
    hash_password,
    verify_password,
    create_session_token,
    get_session_expiry,
)
from app.dependency import get_db
from app.schemas import UserCreate, LoginUser
from app.oauth import oauth
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter_by(email=data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    tier = db.query(models.Tier).filter_by(name="free").first()
    user = models.User(
        email=data.email,
        password_hash=hash_password(data.password),
        tier_id=tier.id
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created"}


@router.post("/login")
def login(
    data: LoginUser,
    response: Response,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter_by(email=data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if user.auth_provider == "google" or user.password_hash is None:
        raise HTTPException(
            status_code=400,
            detail="This account uses Google Sign-In. Please log in with Google."
        )

    if not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    session_token = create_session_token()
    session = models.UserSession(
        session_id=session_token,
        user_id=user.user_id,
        expires_at=get_session_expiry()
    )

    db.add(session)
    db.commit()

    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )

    return {"message": "Logged in"}


@router.get("/google/login")
async def google_login(request: Request):
    return await oauth.google.authorize_redirect(
        request,
        settings.GOOGLE_REDIRECT_URI
    )


@router.get("/google/callback")
async def google_callback(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    google_token = await oauth.google.authorize_access_token(request)

    try:
        user_info = await oauth.google.parse_id_token(request, google_token)
    except KeyError:
        user_info = await oauth.google.userinfo(token=google_token)

    if not user_info or not user_info.get("email_verified"):
        raise HTTPException(status_code=400, detail="Email not verified")

    email = user_info['email']
    google_id = user_info['sub']

    user = db.query(models.User).filter_by(google_id=google_id).first()

    tier = db.query(models.Tier).filter_by(name="google").first()

    if not user:
        user = db.query(models.User).filter_by(email=email).first()

        if user:
            user.google_id = google_id
            user.auth_provider = "google"
            user.tier_id = tier.id
            db.commit()
        else:
            user = models.User(
                email=email,
                google_id=google_id,
                auth_provider="google",
                password_hash=None,
                tier_id=tier.id
            )
            db.add(user)
        db.commit()
        db.refresh(user)

    session_token = create_session_token()
    session = models.UserSession(
        session_id=session_token,
        user_id=user.user_id,
        expires_at=get_session_expiry()
    )
    db.add(session)
    db.commit()

    response = RedirectResponse(settings.FRONTEND_CALLBACK_URL)
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=60 * 60 * 24 * 7,
    )

    return response


@router.post("/logout")
def logout(
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    session_id = request.cookies.get("session_token")

    if session_id:
        session = (
            db.query(models.UserSession)
            .filter(models.UserSession.session_id == session_id)
            .first()
        )

        if session:
            session.is_revoked = True
            db.commit()

    response.delete_cookie(
        key="session_token",
        httponly=True,
        secure=False,
        samesite="lax"
    )
    return {"message": "Logged out successfully"}
