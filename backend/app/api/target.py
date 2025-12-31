from app.api import common as api_common
from app.api.errors import re_raise_as_internal_error
from app.crud import target as crud_target
from app.database import get_db
from app.schemas import target as schema_target
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(tags=["Target"])


@router.get("/targets", response_model=list[schema_target.Target])
def get_targets(
    db: Session = Depends(get_db), _current_user=Depends(api_common.log_token_user)
):
    try:
        return crud_target.get_targets(db)

    except Exception as e:
        re_raise_as_internal_error(e)


@router.post("/targets", response_model=schema_target.Target)
def create_target(
    target: schema_target.TargetCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        result = crud_target.create_target(db, target)
        return result

    except Exception as e:
        re_raise_as_internal_error(e)


@router.put("/targets", response_model=schema_target.Target)
def update_target(
    target: schema_target.TargetUpdate,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        result = crud_target.update_target(db, target)
        return result

    except Exception as e:
        re_raise_as_internal_error(e)


@router.delete("/targets/{rid}", response_model=None)
def delete_target(
    rid: int,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        crud_target.delete_target(db, rid)
        return {"result": "deleted"}

    except Exception as e:
        re_raise_as_internal_error(e)
