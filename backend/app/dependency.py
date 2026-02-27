from datetime import datetime
from app.db import SessionLocal
from app import models
from app.redis import get_redis
from app.services.rate_limiter import RateLimiter
from app.services.ip_rate_limiter import IPRateLimiter
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


def get_client_ip(request: Request) -> str:
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.client.host


def make_ip_rate_limit_dependency(max_requests: int, window_seconds: int):
    """
    Factory that creates a dependency for IP based rate limiting.

    Args:
        max_requests: Maximum number of requests allowed in the window
        window_seconds: Time window in seconds
    """
    def dependency(
        request: Request,
        redis: Redis = Depends(get_redis),
    ):
        ip = get_client_ip(request)
        route = request.url.path
        limiter = IPRateLimiter(redis)
        allowed = limiter.check(ip, route, max_requests, window_seconds)

        if not allowed:
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Too many requests from this IP",
                headers={"Retry-After": str(window_seconds)},
            )

    return dependency


registration_limit = make_ip_rate_limit_dependency(max_requests=3, window_seconds=settings.TTL_SECONDS)
login_limit = make_ip_rate_limit_dependency(max_requests=10,window_seconds=3600)
roast_limit = make_rate_limit_dependency("max_roasts_daily")
