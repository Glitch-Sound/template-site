from datetime import datetime
from zoneinfo import ZoneInfo

from app.api import common as api_common
from app.api.errors import re_raise_as_internal_error
from app.crud import batch as crud_batch
from app.database import SessionLocal, get_db
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(tags=["Batch"])


@router.post("/batch", response_model=None)
def exec_batch(
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        crud_batch.import_number(db)
        crud_batch.import_larte_checklist(db)
        return {"result": "success"}

    except Exception as e:
        re_raise_as_internal_error(e)


JST = ZoneInfo("Asia/Tokyo")


def scheduled_batch() -> None:
    db: Session = SessionLocal()
    try:
        today_str = datetime.now(JST).date().isoformat()
        print("exec: " + today_str)

        crud_batch.import_number(db)
        crud_batch.import_larte_checklist(db)

    finally:
        db.close()
