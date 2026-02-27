from datetime import datetime, timezone
from redis import Redis
from app.models import User
from app.config import settings


class RateLimiter:
    """
    Handles per-user daily rate limiting using Redis as the counter store.
    """

    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    def check(
        self,
        user: User,
        feature: str,
    ) -> tuple[bool, int, int]:
        """
        Returns: (is_allowed, current_count, remaining)
        """
        limit: int = getattr(user.tier, feature)

        # -1 means unlimited (e.g. enterprise tier)
        if limit == -1:
            return True, 0, -1

        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        key = f"{feature}:{user.user_id}:{today}"

        ttl_seconds = settings.TTL_SECONDS
        count = self.redis.incr(key)
        if count == 1:
            self.redis.expire(key, ttl_seconds)

        remaining = max(0, limit - count)
        allowed = count <= limit

        if not allowed:
            self.redis.decr(key)

        return allowed, count, remaining
