import os
from datetime import datetime, timedelta

import jwt
from app.models import user as model_user
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import ExpiredSignatureError, InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy import and_
from sqlalchemy.orm import Session

# fmt: off
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGEME_FOR_PRODUCTION")
ALGORITHM  = "HS256"

SECONDS_EXPIRE_TOKEN_ACCESS  = 3600
SECONDS_EXPIRE_TOKEN_REFRESH = 60 * 60 * 24 * 14  # 2week.

security    = HTTPBearer()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# fmt: on


def verify_password(password_plain: str, password_hashed: str) -> bool:
    return pwd_context.verify(password_plain, password_hashed)


def create_jwt_token_pair(rid_user: int) -> tuple[str, str]:
    # fmt: off
    token_access  = _create_jwt_token({"sub": str(rid_user), "type": "access"},  SECONDS_EXPIRE_TOKEN_ACCESS)
    token_refresh = _create_jwt_token({"sub": str(rid_user), "type": "refresh"}, SECONDS_EXPIRE_TOKEN_REFRESH)
    # fmt: on
    return token_access, token_refresh


def decode_jwt_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])


def get_token_user(
    db: Session, token: HTTPAuthorizationCredentials = Depends(security)
) -> model_user.User:
    try:
        decoded = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])

    except ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=401,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    except InvalidTokenError as exc:
        raise HTTPException(
            status_code=401,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    rid_user = decoded.get("sub")
    return (
        db.query(model_user.User)
        .filter(and_(model_user.User.rid == rid_user, ~model_user.User.is_deleted))
        .first()
    )


def _create_jwt_token(data: dict, expires_delta: int) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    if isinstance(encoded, bytes):
        encoded = encoded.decode("utf-8")
    return encoded
