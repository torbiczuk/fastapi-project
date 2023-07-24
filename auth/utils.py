from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from config import settings

ACCESS_TOKEN_EXPIRE_MINUTES = 15  # 15 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days
ALGORITHM = "HS256"

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def _create_token(subject: str, secret_key: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is None:
        if secret_key == settings.JWT_SECRET_KEY:
            expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        elif secret_key == settings.JWT_REFRESH_SECRET_KEY:
            expires_delta = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, secret_key, ALGORITHM)
    return encoded_jwt


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    return _create_token(subject, settings.JWT_SECRET_KEY, expires_delta)


def create_refresh_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    return _create_token(subject, settings.JWT_REFRESH_SECRET_KEY, expires_delta)
