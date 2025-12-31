from datetime import datetime

from app.models import company as model_company
from app.models import project as model_project
from app.models import project_group as model_project_group
from app.models import summary as model_summary
from app.schemas import summary as schema_summary
from pytz import timezone
from sqlalchemy import Date, cast, func, insert, literal, select
from sqlalchemy.orm import Session

JST = timezone("Asia/Tokyo")


def get_summaries_latest_company_total(
    db: Session,
) -> list[schema_summary.SummaryTotalCompany]:
    latest = select(
        func.max(model_summary.SummaryTotalCompany.date_snap)
    ).scalar_subquery()

    # fmt: off
    query = db.query(
        model_summary.SummaryTotalCompany
    )\
    .filter(
        model_summary.SummaryTotalCompany.date_snap == latest
    )\
    .order_by(model_summary.SummaryTotalCompany.rid_companies, model_summary.SummaryTotalCompany.rid)
    # fmt: on

    return query.all()


def get_summaries_latest_project_total(
    db: Session,
) -> list[schema_summary.SummaryTotalProject]:
    latest = select(
        func.max(model_summary.SummaryTotalProject.date_snap)
    ).scalar_subquery()

    # fmt: off
    query = db.query(
        model_summary.SummaryTotalProject
    )\
    .filter(
        model_summary.SummaryTotalProject.date_snap == latest
    )\
    .order_by(model_summary.SummaryTotalProject.rid_project_groups, model_summary.SummaryTotalProject.rid)
    # fmt: on

    return query.all()


def get_summaries_latest_pm_total(db: Session) -> list[schema_summary.SummaryTotalPM]:
    latest = select(func.max(model_summary.SummaryTotalPM.date_snap)).scalar_subquery()

    # fmt: off
    query = db.query(
        model_summary.SummaryTotalPM
    )\
    .filter(
        model_summary.SummaryTotalPM.date_snap == latest
    )\
    .order_by(model_summary.SummaryTotalPM.rid_users_pm, model_summary.SummaryTotalPM.rid)
    # fmt: on

    return query.all()


def get_summaries_latest_pl_total(db: Session) -> list[schema_summary.SummaryTotalPL]:
    latest = select(func.max(model_summary.SummaryTotalPL.date_snap)).scalar_subquery()

    # fmt: off
    query = db.query(
        model_summary.SummaryTotalPL
    )\
    .filter(
        model_summary.SummaryTotalPL.date_snap == latest
    )\
    .order_by(model_summary.SummaryTotalPL.rid_users_pl, model_summary.SummaryTotalPL.rid)
    # fmt: on

    return query.all()


def get_summaries_latest_company_count(
    db: Session,
) -> list[schema_summary.SummaryCountCompany]:
    latest = select(
        func.max(model_summary.SummaryCountCompany.date_snap)
    ).scalar_subquery()

    # fmt: off
    query = db.query(
        model_summary.SummaryCountCompany
    )\
    .filter(
        model_summary.SummaryCountCompany.date_snap == latest
    )\
    .order_by(model_summary.SummaryCountCompany.rid_companies, model_summary.SummaryCountCompany.rid)
    # fmt: on

    return query.all()


def get_summaries_latest_project_count(
    db: Session,
) -> list[schema_summary.SummaryCountProject]:
    latest = select(
        func.max(model_summary.SummaryCountProject.date_snap)
    ).scalar_subquery()

    # fmt: off
    query = db.query(
        model_summary.SummaryCountProject
    )\
    .filter(
        model_summary.SummaryCountProject.date_snap == latest
    )\
    .order_by(model_summary.SummaryCountProject.rid_project_groups, model_summary.SummaryCountProject.rid)
    # fmt: on

    return query.all()


def get_summaries_latest_pm_count(db: Session) -> list[schema_summary.SummaryCountPM]:
    latest = select(func.max(model_summary.SummaryCountPM.date_snap)).scalar_subquery()

    # fmt: off
    query = db.query(
        model_summary.SummaryCountPM
    )\
    .filter(
        model_summary.SummaryCountPM.date_snap == latest
    )\
    .order_by(model_summary.SummaryCountPM.rid_users_pm, model_summary.SummaryCountPM.rid)
    # fmt: on

    return query.all()


def get_summaries_latest_pl_count(db: Session) -> list[schema_summary.SummaryCountPL]:
    latest = select(func.max(model_summary.SummaryCountPL.date_snap)).scalar_subquery()

    # fmt: off
    query = db.query(
        model_summary.SummaryCountPL
    )\
    .filter(
        model_summary.SummaryCountPL.date_snap == latest
    )\
    .order_by(model_summary.SummaryCountPL.rid_users_pl, model_summary.SummaryCountPL.rid)
    # fmt: on

    return query.all()


def get_summaries_period_company_total(
    db: Session,
    year: int,
) -> list[schema_summary.SummaryTotalCompany]:
    # fmt: off
    query = db.query(
        model_summary.SummaryTotalCompany
    )\
    .filter(
        model_summary.SummaryTotalCompany.date_snap.startswith(f"{year}-")
    )\
    .order_by(model_summary.SummaryTotalCompany.rid_companies, model_summary.SummaryTotalCompany.rid)
    # fmt: on

    return query.all()


def get_summaries_period_project_total(
    db: Session,
    year: int,
) -> list[schema_summary.SummaryTotalProject]:
    # fmt: off
    query = db.query(
        model_summary.SummaryTotalProject
    )\
    .filter(
        model_summary.SummaryTotalProject.date_snap.startswith(f"{year}-")
    )\
    .order_by(model_summary.SummaryTotalProject.rid_project_groups, model_summary.SummaryTotalProject.rid)
    # fmt: on

    return query.all()


def get_summaries_period_pm_total(
    db: Session,
    year: int,
) -> list[schema_summary.SummaryTotalPM]:
    # fmt: off
    query = db.query(
        model_summary.SummaryTotalPM
    )\
    .filter(
        model_summary.SummaryTotalPM.date_snap.startswith(f"{year}-")
    )\
    .order_by(model_summary.SummaryTotalPM.rid_users_pm, model_summary.SummaryTotalPM.rid)
    # fmt: on

    return query.all()


def get_summaries_period_pl_total(
    db: Session,
    year: int,
) -> list[schema_summary.SummaryTotalPL]:
    # fmt: off
    query = db.query(
        model_summary.SummaryTotalPL
    )\
    .filter(
        model_summary.SummaryTotalPL.date_snap.startswith(f"{year}-")
    )\
    .order_by(model_summary.SummaryTotalPL.rid_users_pl, model_summary.SummaryTotalPL.rid)
    # fmt: on

    return query.all()


def get_summaries_period_company_count(
    db: Session,
    year: int,
) -> list[schema_summary.SummaryCountCompany]:
    # fmt: off
    query = db.query(
        model_summary.SummaryCountCompany
    )\
    .filter(
        model_summary.SummaryCountCompany.date_snap.startswith(f"{year}-")
    )\
    .order_by(model_summary.SummaryCountCompany.rid_companies, model_summary.SummaryCountCompany.rid)
    # fmt: on

    return query.all()


def get_summaries_period_project_count(
    db: Session,
    year: int,
) -> list[schema_summary.SummaryCountProject]:
    # fmt: off
    query = db.query(
        model_summary.SummaryCountProject
    )\
    .filter(
        model_summary.SummaryCountProject.date_snap.startswith(f"{year}-")
    )\
    .order_by(model_summary.SummaryCountProject.rid_project_groups, model_summary.SummaryCountProject.rid)
    # fmt: on

    return query.all()


def get_summaries_period_pm_count(
    db: Session,
    year: int,
) -> list[schema_summary.SummaryCountPM]:
    # fmt: off
    query = db.query(
        model_summary.SummaryCountPM
    )\
    .filter(
        model_summary.SummaryCountPM.date_snap.startswith(f"{year}-")
    )\
    .order_by(model_summary.SummaryCountPM.rid_users_pm, model_summary.SummaryCountPM.rid)
    # fmt: on

    return query.all()


def get_summaries_period_pl_count(
    db: Session,
    year: int,
) -> list[schema_summary.SummaryCountPL]:
    # fmt: off
    query = db.query(
        model_summary.SummaryCountPL
    )\
    .filter(
        model_summary.SummaryCountPL.date_snap.startswith(f"{year}-")
    )\
    .order_by(model_summary.SummaryCountPL.rid_users_pl, model_summary.SummaryCountPL.rid)
    # fmt: on

    return query.all()


def create_summaries(
    db: Session,
    target: schema_summary.SummaryCreate,
) -> None:
    target_date = (target.date_snap or "").strip()
    snapshot_date = target_date or _today_jst()
    filters = _get_filter(target_date)
    try:
        _clear_summaries(db, snapshot_date)
        _create_summaries_company_total(db, filters, snapshot_date)
        _create_summaries_project_total(db, filters, snapshot_date)
        _create_summaries_pm_total(db, filters, snapshot_date)
        _create_summaries_pl_total(db, filters, snapshot_date)
        _create_summaries_company_count(db, filters, snapshot_date)
        _create_summaries_project_count(db, filters, snapshot_date)
        _create_summaries_pm_count(db, filters, snapshot_date)
        _create_summaries_pl_count(db, filters, snapshot_date)
        db.commit()

    except Exception:
        db.rollback()
        raise


def _clear_summaries(db: Session, snapshot_date: str) -> None:
    db.query(model_summary.SummaryTotalCompany).filter(
        model_summary.SummaryTotalCompany.date_snap == snapshot_date
    ).delete(synchronize_session=False)
    db.query(model_summary.SummaryTotalProject).filter(
        model_summary.SummaryTotalProject.date_snap == snapshot_date
    ).delete(synchronize_session=False)
    db.query(model_summary.SummaryTotalPM).filter(
        model_summary.SummaryTotalPM.date_snap == snapshot_date
    ).delete(synchronize_session=False)
    db.query(model_summary.SummaryTotalPL).filter(
        model_summary.SummaryTotalPL.date_snap == snapshot_date
    ).delete(synchronize_session=False)
    db.query(model_summary.SummaryCountCompany).filter(
        model_summary.SummaryCountCompany.date_snap == snapshot_date
    ).delete(synchronize_session=False)
    db.query(model_summary.SummaryCountProject).filter(
        model_summary.SummaryCountProject.date_snap == snapshot_date
    ).delete(synchronize_session=False)
    db.query(model_summary.SummaryCountPM).filter(
        model_summary.SummaryCountPM.date_snap == snapshot_date
    ).delete(synchronize_session=False)
    db.query(model_summary.SummaryCountPL).filter(
        model_summary.SummaryCountPL.date_snap == snapshot_date
    ).delete(synchronize_session=False)


def _create_summaries_company_total(
    db: Session,
    filters: list,
    snapshot_date: str,
) -> None:
    # fmt: off
    summary = (
        select(
            literal(snapshot_date).label("date_snap"),
            model_company.Company.rid.label("rid_companies"),
            func.sum(model_project.Project.amount_expected).label("total_expected"),
            func.sum(model_project.Project.amount_order).label("total_order"),
        )
        .select_from(model_project.Project)
        .join(
            model_project_group.ProjectGroup,
            model_project.Project.rid_project_groups == model_project_group.ProjectGroup.rid,
        )
        .join(
            model_company.Company,
            model_project_group.ProjectGroup.rid_companies == model_company.Company.rid,
        )
        .where(*filters)
        .group_by(model_company.Company.rid)
        .order_by(model_company.Company.rid)
    )
    # fmt: on

    stmt = insert(model_summary.SummaryTotalCompany).from_select(
        ["date_snap", "rid_companies", "total_expected", "total_order"],
        summary,
    )
    db.execute(stmt)


def _create_summaries_project_total(
    db: Session,
    filters: list,
    snapshot_date: str,
) -> None:
    # fmt: off
    summary = (
        select(
            literal(snapshot_date).label("date_snap"),
            model_project_group.ProjectGroup.rid.label("rid_project_groups"),
            func.sum(model_project.Project.amount_expected).label("total_expected"),
            func.sum(model_project.Project.amount_order).label("total_order"),
        )
        .select_from(model_project.Project)
        .join(
            model_project_group.ProjectGroup,
            model_project.Project.rid_project_groups == model_project_group.ProjectGroup.rid,
        )
        .where(*filters)
        .group_by(model_project_group.ProjectGroup.rid)
        .order_by(model_project_group.ProjectGroup.rid)
    )
    # fmt: on

    stmt = insert(model_summary.SummaryTotalProject).from_select(
        ["date_snap", "rid_project_groups", "total_expected", "total_order"],
        summary,
    )
    db.execute(stmt)


def _create_summaries_pm_total(
    db: Session,
    filters: list,
    snapshot_date: str,
) -> None:
    # fmt: off
    summary = (
        select(
            literal(snapshot_date).label("date_snap"),
            model_project.Project.rid_users_pm.label("rid_users_pm"),
            func.sum(model_project.Project.amount_expected).label("total_expected"),
            func.sum(model_project.Project.amount_order).label("total_order"),
        )
        .select_from(model_project.Project)
        .where(*filters)
        .group_by(model_project.Project.rid_users_pm)
        .order_by(model_project.Project.rid_users_pm)
    )
    # fmt: on

    stmt = insert(model_summary.SummaryTotalPM).from_select(
        ["date_snap", "rid_users_pm", "total_expected", "total_order"],
        summary,
    )
    db.execute(stmt)


def _create_summaries_pl_total(
    db: Session,
    filters: list,
    snapshot_date: str,
) -> None:
    # fmt: off
    summary = (
        select(
            literal(snapshot_date).label("date_snap"),
            model_project.Project.rid_users_pl.label("rid_users_pl"),
            func.sum(model_project.Project.amount_expected).label("total_expected"),
            func.sum(model_project.Project.amount_order).label("total_order"),
        )
        .select_from(model_project.Project)
        .where(*filters)
        .group_by(model_project.Project.rid_users_pl)
        .order_by(model_project.Project.rid_users_pl)
    )
    # fmt: on

    stmt = insert(model_summary.SummaryTotalPL).from_select(
        ["date_snap", "rid_users_pl", "total_expected", "total_order"],
        summary,
    )
    db.execute(stmt)


def _create_summaries_company_count(
    db: Session,
    filters: list,
    snapshot_date: str,
) -> None:
    # fmt: off
    summary = (
        select(
            literal(snapshot_date).label("date_snap"),
            model_company.Company.rid.label("rid_companies"),
            model_project.Project.rank.label("rank"),
            func.count(model_company.Company.rid).label("count"),
        )
        .select_from(model_project.Project)
        .join(
            model_project_group.ProjectGroup,
            model_project.Project.rid_project_groups == model_project_group.ProjectGroup.rid,
        )
        .join(
            model_company.Company,
            model_project_group.ProjectGroup.rid_companies == model_company.Company.rid,
        )
        .where(*filters)
        .group_by(model_company.Company.rid, model_project.Project.rank)
        .order_by(model_company.Company.rid, model_project.Project.rank)
    )
    # fmt: on

    stmt = insert(model_summary.SummaryCountCompany).from_select(
        ["date_snap", "rid_companies", "rank", "count"],
        summary,
    )
    db.execute(stmt)


def _create_summaries_project_count(
    db: Session,
    filters: list,
    snapshot_date: str,
) -> None:
    # fmt: off
    summary = (
        select(
            literal(snapshot_date).label("date_snap"),
            model_project_group.ProjectGroup.rid.label("rid_project_groups"),
            model_project.Project.rank.label("rank"),
            func.count(model_project_group.ProjectGroup.rid).label("count"),
        )
        .select_from(model_project.Project)
        .join(
            model_project_group.ProjectGroup,
            model_project.Project.rid_project_groups == model_project_group.ProjectGroup.rid,
        )
        .where(*filters)
        .group_by(model_project_group.ProjectGroup.rid, model_project.Project.rank)
        .order_by(model_project_group.ProjectGroup.rid, model_project.Project.rank)
    )
    # fmt: on

    stmt = insert(model_summary.SummaryCountProject).from_select(
        ["date_snap", "rid_project_groups", "rank", "count"],
        summary,
    )
    db.execute(stmt)


def _create_summaries_pm_count(
    db: Session,
    filters: list,
    snapshot_date: str,
) -> None:
    # fmt: off
    summary = (
        select(
            literal(snapshot_date).label("date_snap"),
            model_project.Project.rid_users_pm.label("rid_users_pm"),
            model_project.Project.rank.label("rank"),
            func.count(model_project.Project.rid_users_pm).label("count"),
        )
        .select_from(model_project.Project)
        .where(*filters)
        .group_by(model_project.Project.rid_users_pm, model_project.Project.rank)
        .order_by(model_project.Project.rid_users_pm, model_project.Project.rank)
    )
    # fmt: on

    stmt = insert(model_summary.SummaryCountPM).from_select(
        ["date_snap", "rid_users_pm", "rank", "count"],
        summary,
    )
    db.execute(stmt)


def _create_summaries_pl_count(
    db: Session,
    filters: list,
    snapshot_date: str,
) -> None:
    # fmt: off
    summary = (
        select(
            literal(snapshot_date).label("date_snap"),
            model_project.Project.rid_users_pl.label("rid_users_pl"),
            model_project.Project.rank.label("rank"),
            func.count(model_project.Project.rid_users_pl).label("count"),
        )
        .select_from(model_project.Project)
        .where(*filters)
        .group_by(model_project.Project.rid_users_pl, model_project.Project.rank)
        .order_by(model_project.Project.rid_users_pl, model_project.Project.rank)
    )
    # fmt: on

    stmt = insert(model_summary.SummaryCountPL).from_select(
        ["date_snap", "rid_users_pl", "rank", "count"],
        summary,
    )
    db.execute(stmt)


def _get_filter(date_limit: str | None) -> list:
    where_clauses = [
        model_project.Project.is_deleted.is_(False),
    ]

    if date_limit:
        where_clauses.append(
            cast(model_project.Project.updated_at, Date)
            <= func.date(literal(date_limit))
        )
    return where_clauses


def _today_jst() -> str:
    return datetime.now(JST).date().isoformat()
