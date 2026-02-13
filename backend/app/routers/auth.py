from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from datetime import datetime
from app.db import SessionLocal
from app import models
from app.auth import (
    hash_password,
    verify_password,
    create_session_token,
    get_session_expiry,
)
from app.dependency import get_db
from app.schemas import UserCreate, LoginUser

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(data: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter_by(email=data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(
        email=data.email,
        password_hash=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"message": "User created"}


@router.post("/login")
def login(
    data:LoginUser,
    response: Response,
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter_by(email=data.email).first()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_session_token()
    session = models.UserSession(
        session_id=token,
        user_id=user.user_id,
        expires_at=get_session_expiry()
    )

    db.add(session)
    db.commit()

    # Set secure cookie
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        secure=False,   # True in prod (HTTPS)
        samesite="lax"
    )

    return {"message": "Logged in"}


@router.post("/logout")
def logout(response: Response, db: Session = Depends(get_db)):
    response.delete_cookie("session_token")
    return {"message": "Logged out"}
