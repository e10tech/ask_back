import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Any, Dict

import jwt
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)


def generate_token(length: int = 48) -> str:
    return secrets.token_urlsafe(length)


def hash_refresh_token(refresh_token: str) -> str:
    return hashlib.sha256(refresh_token.encode("utf-8")).hexdigest()


def now_utc() -> datetime:
    return datetime.utcnow()


def create_access_token(
    data: Dict[str, Any],
    secret: str,
    expires_minutes: int,
) -> str:
    to_encode = data.copy()
    expire = now_utc() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret, algorithm="HS256")
