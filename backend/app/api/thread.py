from app.api import common as api_common
from app.api.errors import re_raise_as_internal_error
from app.crud import thread as crud_thread
from app.database import get_db
from app.schemas import thread as schema_thread
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(tags=["Thread"])


@router.get("/threads/status", response_model=list[schema_thread.ThreadStatus])
def get_threads_status(
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_thread.get_threads_status(db)

    except Exception as e:
        re_raise_as_internal_error(e)


@router.get("/threads/{rid}", response_model=list[schema_thread.Thread])
def get_threads_by_rid(
    rid: int,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_thread.get_threads_by_rid(db, rid)

    except Exception as e:
        re_raise_as_internal_error(e)


@router.post("/threads", response_model=schema_thread.Thread)
def create_thread(
    target: schema_thread.ThreadCreate,
    db: Session = Depends(get_db),
    current_user=Depends(api_common.log_token_user),
):
    try:
        result = crud_thread.create_thread(db, target, current_user)
        return result

    except Exception as e:
        re_raise_as_internal_error(e)


@router.put("/threads", response_model=schema_thread.Thread)
def update_thread(
    target: schema_thread.ThreadUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(api_common.log_token_user),
):
    try:
        result = crud_thread.update_thread(db, target, current_user)
        return result

    except Exception as e:
        re_raise_as_internal_error(e)


@router.delete("/threads/{rid}", response_model=None)
def delete_thread(
    rid: int,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        crud_thread.delete_thread(db, rid)
        return {"result": "deleted"}

    except Exception as e:
        re_raise_as_internal_error(e)
