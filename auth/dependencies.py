from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt

from auth.utils import (
    ALGORITHM,
)
from config import settings


def _validate_token(secret_key: str, token: str):
    try:
        payload = jwt.decode(token, secret_key, ALGORITHM)
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


def validate_access_token(token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    return _validate_token(settings.JWT_SECRET_KEY, token.credentials)


def validate_refresh_token(token: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    return _validate_token(settings.JWT_REFRESH_SECRET_KEY, token.credentials)


def validate_websocket_jwt_token(token) -> dict:
    return _validate_token(settings.JWT_SECRET_KEY, token)
