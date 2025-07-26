import jwt
from app.crud import auth as crud_auth
from app.crud import user as crud_user
from app.database import get_db
from app.schemas import auth as schemas_auth
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

router = APIRouter(tags=["Auth"])


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
            token_access=token_access, token_refresh=token_refresh
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/refresh", response_model=schemas_auth.Token)
def refresh(data: schemas_auth.Refresh):
    try:
        decoded = crud_auth.decode_jwt_token(data.token_refresh)
        if decoded.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid refresh token"
            )

        user_id = decoded["sub"]
        token_access, token_refresh = crud_auth.create_jwt_token_pair(user_id)
        return schemas_auth.Token(
            token_access=token_access, token_refresh=token_refresh
        )

    except jwt.ExpiredSignatureError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired"
        ) from exc

    except jwt.InvalidTokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from exc

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
