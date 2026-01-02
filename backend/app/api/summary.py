from datetime import datetime
from zoneinfo import ZoneInfo

from app.api import common as api_common
from app.api.errors import re_raise_as_internal_error
from app.crud import summary as crud_summary
from app.database import SessionLocal, get_db
from app.schemas import project as schema_project
from app.schemas import summary as schema_summary
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(tags=["Summary"])


@router.get(
    "/summaries/amount/latest",
    response_model=list[schema_summary.SummaryAmount],
)
def get_summaries_amount_latest(
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_amount_latest(db)
    except Exception as e:
        re_raise_as_internal_error(e)


@router.get(
    "/summaries/amount/{year}",
    response_model=list[schema_summary.SummaryAmount],
)
def get_summaries_amount(
    year: int,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_amount(db, year)
    except Exception as e:
        re_raise_as_internal_error(e)


@router.get(
    "/summaries/company/latest",
    response_model=list[schema_summary.SummaryCompany],
)
def get_summaries_company_latest(
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_company_latest(db)
    except Exception as e:
        re_raise_as_internal_error(e)


@router.get(
    "/summaries/company/{year}",
    response_model=list[schema_summary.SummaryCompany],
)
def get_summaries_company(
    year: int,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_company(db, year)
    except Exception as e:
        re_raise_as_internal_error(e)


@router.post("/summaries", response_model=None)
def create_summaries(
    target: schema_summary.SummaryCreate,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        crud_summary.create_summaries(db, target)
        return {"result": "success"}

    except Exception as e:
        re_raise_as_internal_error(e)


JST = ZoneInfo("Asia/Tokyo")


def scheduled_summaries() -> None:
    db: Session = SessionLocal()
    try:
        today_str = datetime.now(JST).date().isoformat()
        print("summary: " + today_str)

        target = schema_summary.SummaryCreate(date_snap=today_str)
        crud_summary.create_summaries(db, target)

    finally:
        db.close()


@router.get(
    "/summaries/deadline",
    response_model=list[schema_project.Project],
)
def get_summaries_deadline(
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_deadline(db)
    except Exception as e:
        re_raise_as_internal_error(e)


@router.get(
    "/summaries/incomplete",
    response_model=list[schema_project.Project],
)
def get_summaries_incomplete(
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_incomplete(db)
    except Exception as e:
        re_raise_as_internal_error(e)


@router.get(
    "/summaries/alert",
    response_model=list[schema_project.Project],
)
def get_summaries_alert(
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_alert(db)
    except Exception as e:
        re_raise_as_internal_error(e)
