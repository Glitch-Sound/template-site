from app.api import common as api_common
from app.crud import user as crud_user
from app.database import get_db
from app.schemas import user as schema_user
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

router = APIRouter(tags=["User"])


@router.get("/users", response_model=list[schema_user.User])
def get_users(
    db: Session = Depends(get_db), _current_user=Depends(api_common.log_token_user)
):
    try:
        return crud_user.get_users(db)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/users/{rid}", response_model=schema_user.User)
def get_user_by_rid(
    rid: int,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_user.get_user_by_rid(db, rid)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/users", response_model=schema_user.User)
def create_user(
    target: schema_user.UserCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        result = crud_user.create_user(db, target)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.put("/users", response_model=schema_user.User)
def update_user(
    target: schema_user.UserUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        result = crud_user.update_user(db, target)
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/users/{rid}", response_model=None)
def delete_user(
    rid: int,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        crud_user.delete_user(db, rid)
        return {"result": "deleted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
