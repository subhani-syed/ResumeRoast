from datetime import datetime
from app.db import SessionLocal
from app import models
from app.redis import get_redis
from app.services.rate_limiter import RateLimiter
from app.config import settings
from fastapi import Depends, HTTPException, Request, status, Response
from sqlalchemy.orm import Session
from redis import Redis


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

    if session.is_revoked:
        raise HTTPException(status_code=401, detail="Session revoked")

    if session.expires_at < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Session expired")

    user = db.query(models.User).get(session.user_id)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def make_rate_limit_dependency(feature: str):
    """
    Factory that creates a dependency for rate limiting a specific feature.

    Args:
        feature: Tier attribute name to limit against (e.g. "max_roasts_daily")
    """
    def dependency(
        response: Response,
        user: models.User = Depends(get_current_user),
        redis: Redis = Depends(get_redis),
    ):
        limiter = RateLimiter(redis)
        allowed, count, remaining = limiter.check(user, feature)

        limit_value = getattr(user.tier, feature)
        response.headers["X-RateLimit-Limit"] = str(limit_value)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        response.headers["X-RateLimit-Feature"] = feature

        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"Daily limit reached for {feature.replace('_', ' ')}",
                headers={"Retry-After": f"{settings.TTL_SECONDS}"},
            )
        return user

    return dependency


roast_limit = make_rate_limit_dependency("max_roasts_daily")
