from passlib.context import CryptContext
import secrets
from datetime import datetime, timedelta
import hashlib

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SESSION_EXPIRE_MINUTES = 60 * 24  # 1 day

def normalize_password(password: str) -> bytes:
    return hashlib.sha256(password.encode("utf-8")).digest()

def hash_password(password: str) -> str:
    normalized = normalize_password(password)
    return pwd_context.hash(normalized)

def verify_password(password: str, hashed: str) -> bool:
    normalized = normalize_password(password)
    return pwd_context.verify(normalized, hashed)

def create_session_token() -> str:
    return secrets.token_urlsafe(32)

def get_session_expiry():
    return datetime.utcnow() + timedelta(minutes=SESSION_EXPIRE_MINUTES)
