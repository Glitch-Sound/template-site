from datetime import datetime
from zoneinfo import ZoneInfo

from app.api import common as api_common
from app.api.errors import re_raise_as_internal_error
from app.crud import summary as crud_summary
from app.database import SessionLocal, get_db
from app.schemas import summary as schema_summary
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter(tags=["Summary"])


@router.get(
    "/summaries/latest/company/total",
    response_model=list[schema_summary.SummaryTotalCompany],
)
def get_summaries_latest_company_total(
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_latest_company_total(db)

    except Exception as e:
        re_raise_as_internal_error(e)


@router.get(
    "/summaries/latest/project/total",
    response_model=list[schema_summary.SummaryTotalProject],
)
def get_summaries_latest_project_total(
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_latest_project_total(db)

    except Exception as e:
        re_raise_as_internal_error(e)


@router.get(
    "/summaries/latest/pm/total",
    response_model=list[schema_summary.SummaryTotalPM],
)
def get_summaries_latest_pm_total(
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_latest_pm_total(db)

    except Exception as e:
        re_raise_as_internal_error(e)


@router.get(
    "/summaries/latest/pl/total",
    response_model=list[schema_summary.SummaryTotalPL],
)
def get_summaries_latest_pl_total(
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_latest_pl_total(db)

    except Exception as e:
        re_raise_as_internal_error(e)


@router.get(
    "/summaries/latest/company/count",
    response_model=list[schema_summary.SummaryCountCompany],
)
def get_summaries_latest_company_count(
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_latest_company_count(db)

    except Exception as e:
        re_raise_as_internal_error(e)


@router.get(
    "/summaries/latest/project/count",
    response_model=list[schema_summary.SummaryCountProject],
)
def get_summaries_latest_project_count(
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_latest_project_count(db)

    except Exception as e:
        re_raise_as_internal_error(e)


@router.get(
    "/summaries/latest/pm/count",
    response_model=list[schema_summary.SummaryCountPM],
)
def get_summaries_latest_pm_count(
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_latest_pm_count(db)

    except Exception as e:
        re_raise_as_internal_error(e)


@router.get(
    "/summaries/latest/pl/count",
    response_model=list[schema_summary.SummaryCountPL],
)
def get_summaries_latest_pl_count(
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_latest_pl_count(db)

    except Exception as e:
        re_raise_as_internal_error(e)


@router.get(
    "/summaries/period/company/total/{year}",
    response_model=list[schema_summary.SummaryTotalCompany],
)
def get_summaries_period_company_total(
    year: int,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_period_company_total(db, year)

    except Exception as e:
        re_raise_as_internal_error(e)


@router.get(
    "/summaries/period/project/total/{year}",
    response_model=list[schema_summary.SummaryTotalProject],
)
def get_summaries_period_project_total(
    year: int,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_period_project_total(db, year)

    except Exception as e:
        re_raise_as_internal_error(e)


@router.get(
    "/summaries/period/pm/total/{year}",
    response_model=list[schema_summary.SummaryTotalPM],
)
def get_summaries_period_pm_total(
    year: int,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_period_pm_total(db, year)

    except Exception as e:
        re_raise_as_internal_error(e)


@router.get(
    "/summaries/period/pl/total/{year}",
    response_model=list[schema_summary.SummaryTotalPL],
)
def get_summaries_period_pl_total(
    year: int,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_period_pl_total(db, year)

    except Exception as e:
        re_raise_as_internal_error(e)


@router.get(
    "/summaries/period/company/count/{year}",
    response_model=list[schema_summary.SummaryCountCompany],
)
def get_summaries_period_company_count(
    year: int,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_period_company_count(db, year)

    except Exception as e:
        re_raise_as_internal_error(e)


@router.get(
    "/summaries/period/project/count/{year}",
    response_model=list[schema_summary.SummaryCountProject],
)
def get_summaries_period_project_count(
    year: int,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_period_project_count(db, year)

    except Exception as e:
        re_raise_as_internal_error(e)


@router.get(
    "/summaries/period/pm/count/{year}",
    response_model=list[schema_summary.SummaryCountPM],
)
def get_summaries_period_pm_count(
    year: int,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_period_pm_count(db, year)

    except Exception as e:
        re_raise_as_internal_error(e)


@router.get(
    "/summaries/period/pl/count/{year}",
    response_model=list[schema_summary.SummaryCountPL],
)
def get_summaries_period_pl_count(
    year: int,
    db: Session = Depends(get_db),
    _current_user=Depends(api_common.log_token_user),
):
    try:
        return crud_summary.get_summaries_period_pl_count(db, year)

    except Exception as e:
        re_raise_as_internal_error(e)


@router.post("/summaries", response_model=None)
def create_thread(
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
        target = schema_summary.SummaryCreate(date_snap=today_str)
        crud_summary.create_summaries(db, target)
    finally:
        db.close()
