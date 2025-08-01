import logging

from app.crud import auth as crud_auth
from app.database import get_db
from app.models import user as model_user
from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

logger = logging.getLogger("app.api")
security = HTTPBearer()


def log_token_user(
    db: Session = Depends(get_db),
    token: HTTPAuthorizationCredentials = Depends(security),
):
    user = crud_auth.get_token_user(db, token)
    _log_api(user)
    return user


def _log_api(user: model_user.User) -> None:
    logger.info("API: /user, User: %s / %s", user.rid, user.username)
