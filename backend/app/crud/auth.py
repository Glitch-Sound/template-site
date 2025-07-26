import os
from datetime import datetime, timedelta

import jwt
from passlib.context import CryptContext

# fmt: off
SECRET_KEY = os.getenv("SECRET_KEY", "CHANGEME_FOR_PRODUCTION")
ALGORITHM  = "HS256"

SECONDS_EXPIRE_TOKEN_ACCESS  = 3600
SECONDS_EXPIRE_TOKEN_REFRESH = 60 * 60 * 24 * 14  # 2week.
# fmt: on

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password_plain: str, password_hashed: str) -> bool:
    return pwd_context.verify(password_plain, password_hashed)


def create_jwt_token(data: dict, expires_delta: int) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=expires_delta)
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    if isinstance(encoded, bytes):
        encoded = encoded.decode("utf-8")
    return encoded


def create_jwt_token_pair(user_id: int) -> tuple[str, str]:
    # fmt: off
    token_access  = create_jwt_token({"sub": str(user_id), "type": "access"},  SECONDS_EXPIRE_TOKEN_ACCESS)
    token_refresh = create_jwt_token({"sub": str(user_id), "type": "refresh"}, SECONDS_EXPIRE_TOKEN_REFRESH)
    # fmt: on
    return token_access, token_refresh


def decode_jwt_token(token: str) -> dict:
    decoded = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    return decoded
