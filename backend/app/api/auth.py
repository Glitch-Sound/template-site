from app.api.errors import re_raise_as_internal_error
from app.crud import auth as crud_auth
from app.crud import user as crud_user
from app.database import get_db
from app.schemas import auth as schemas_auth
from app.schemas import user as schema_user
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(tags=["Auth"])


@router.get("/setup/status", response_model=schemas_auth.Status)
def get_status(db: Session = Depends(get_db)):
    try:
        list_user = crud_user.get_users(db)
        if 0 < len(list_user):
            return schemas_auth.Status(is_setup=True)
        else:
            return schemas_auth.Status(is_setup=False)

    except Exception as e:
        re_raise_as_internal_error(e)


@router.post("/setup/admin", response_model=schema_user.User)
def create_user(target: schema_user.UserCreate, db: Session = Depends(get_db)):
    try:
        result = crud_user.create_user(db, target)
        return result

    except Exception as e:
        re_raise_as_internal_error(e)


@router.post("/login", response_model=schemas_auth.Token)
def login(data: schemas_auth.Login, db: Session = Depends(get_db)):
    try:
        user = crud_user.get_user_by_username(db, data.username)
        if not user or not crud_auth.verify_password(data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )

        token_access, token_refresh = crud_auth.create_jwt_token_pair(user.rid)
        return schemas_auth.Token(
            rid=user.rid, token_access=token_access, token_refresh=token_refresh
        )

    except Exception as e:
        re_raise_as_internal_error(e)


@router.post("/refresh", response_model=schemas_auth.Token)
def refresh(data: schemas_auth.Refresh):
    try:
        decoded = crud_auth.decode_jwt_token(data.token_refresh)
        if decoded.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        rid_user = decoded["sub"]
        token_access, token_refresh = crud_auth.create_jwt_token_pair(rid_user)
        return schemas_auth.Token(
            rid=rid_user, token_access=token_access, token_refresh=token_refresh
        )

    except Exception as e:
        re_raise_as_internal_error(e)
