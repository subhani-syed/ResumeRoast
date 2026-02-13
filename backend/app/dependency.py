from app.db import SessionLocal
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app import models
from datetime import datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    session = (
        db.query(models.UserSession)
        .filter(models.UserSession.session_id == session_token)
        .first()
    )

    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")

    if session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Session expired")

    user = db.query(models.User).get(session.user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user
