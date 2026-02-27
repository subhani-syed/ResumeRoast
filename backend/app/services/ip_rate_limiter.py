from datetime import datetime, timezone
from redis import Redis


class IPRateLimiter:
    """
    Handles per-IP rate limiting using Redis as the counter store.
    """

    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    def check(self, ip: str, route: str, max_requests: int, window_seconds: int) -> bool:
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        key = f"ip:{ip}:{route}:{today}"

        count = self.redis.incr(key)
        if count == 1:
            self.redis.expire(key, window_seconds)

        allowed = count <= max_requests
        if not allowed:
            self.redis.decr(key)

        return allowed
