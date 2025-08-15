from app.models import company as model_company
from app.models import project as model_project
from app.models import project_group as model_project_group
from app.models import summary as model_summary
from app.schemas import summary as schema_summary
from sqlalchemy import Date, cast, func, insert, literal, select
from sqlalchemy.orm import Session


def get_summaries_latest_company_total(
    db: Session,
) -> list[schema_summary.SummaryTotalCompany]:
    return None


def get_summaries_latest_project_total(
    db: Session,
) -> list[schema_summary.SummaryTotalProject]:
    return None


def get_summaries_latest_pm_total(db: Session) -> list[schema_summary.SummaryTotalPM]:
    return None


def get_summaries_latest_pl_total(db: Session) -> list[schema_summary.SummaryTotalPL]:
    return None


def get_summaries_latest_company_count(
    db: Session,
) -> list[schema_summary.SummaryCountCompany]:
    return None


def get_summaries_latest_project_count(
    db: Session,
) -> list[schema_summary.SummaryCountProject]:
    return None


def get_summaries_latest_pm_count(db: Session) -> list[schema_summary.SummaryCountPM]:
    return None


def get_summaries_latest_pl_count(db: Session) -> list[schema_summary.SummaryCountPL]:
    return None


def get_summaries_period_company_total(
    db: Session,
    year: int,
    quarter: model_project.TypeQuarter,
) -> list[schema_summary.SummaryTotalCompany]:
    return None


def get_summaries_period_project_total(
    db: Session,
    year: int,
    quarter: model_project.TypeQuarter,
) -> list[schema_summary.SummaryTotalProject]:
    return None


def get_summaries_period_pm_total(
    db: Session,
    year: int,
    quarter: model_project.TypeQuarter,
) -> list[schema_summary.SummaryTotalPM]:
    return None


def get_summaries_period_pl_total(
    db: Session,
    year: int,
    quarter: model_project.TypeQuarter,
) -> list[schema_summary.SummaryTotalPL]:
    return None


def get_summaries_period_company_count(
    db: Session,
    year: int,
    quarter: model_project.TypeQuarter,
) -> list[schema_summary.SummaryCountCompany]:
    return None


def get_summaries_period_project_count(
    db: Session,
    year: int,
    quarter: model_project.TypeQuarter,
) -> list[schema_summary.SummaryCountProject]:
    return None


def get_summaries_period_pm_count(
    db: Session,
    year: int,
    quarter: model_project.TypeQuarter,
) -> list[schema_summary.SummaryCountPM]:
    return None


def get_summaries_period_pl_count(
    db: Session,
    year: int,
    quarter: model_project.TypeQuarter,
) -> list[schema_summary.SummaryCountPL]:
    return None


def create_summaries(
    db: Session,
    target: schema_summary.SummaryCreate,
) -> None:
    try:
        _create_summaries_company_total(db, target)
        _create_summaries_project_total(db, target)
        _create_summaries_pm_total(db, target)
        _create_summaries_pl_total(db, target)
        _create_summaries_company_count(db, target)
        _create_summaries_project_count(db, target)
        _create_summaries_pm_count(db, target)
        _create_summaries_pl_count(db, target)
        db.commit()

    except Exception:
        db.rollback()
        raise


def _create_summaries_company_total(
    db: Session,
    target: schema_summary.SummaryCreate,
) -> None:
    # fmt: off
    summary = (
        select(
            func.date("now", "localtime").label("date_snap"),
            literal(model_summary.TypeSummary.COMPANY.value).label("type"),
            model_company.Company.rid.label("rid_dim"),
            func.sum(model_project.Project.amount_expected).label("expected"),
            func.sum(model_project.Project.amount_order).label("order"),
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
        .where(*_get_filter(target))
        .group_by(model_company.Company.rid)
        .order_by(model_company.Company.rid)
    )
    _insert_summary_total(db, summary)
    # fmt: on


def _create_summaries_project_total(
    db: Session,
    target: schema_summary.SummaryCreate,
) -> None:
    # fmt: off
    summary = (
        select(
            func.date("now", "localtime").label("date_snap"),
            literal(model_summary.TypeSummary.PROJECT.value).label("type"),
            model_project_group.ProjectGroup.rid.label("rid_dim"),
            func.sum(model_project.Project.amount_expected).label("expected"),
            func.sum(model_project.Project.amount_order).label("order"),
        )
        .select_from(model_project.Project)
        .join(
            model_project_group.ProjectGroup,
            model_project.Project.rid_project_groups == model_project_group.ProjectGroup.rid,
        )
        .where(*_get_filter(target))
        .group_by(model_project_group.ProjectGroup.rid)
        .order_by(model_project_group.ProjectGroup.rid)
    )
    _insert_summary_total(db, summary)
    # fmt: on


def _create_summaries_pm_total(
    db: Session,
    target: schema_summary.SummaryCreate,
) -> None:
    # fmt: off
    summary = (
        select(
            func.date("now", "localtime").label("date_snap"),
            literal(model_summary.TypeSummary.USER_PM.value).label("type"),
            model_project.Project.rid_users_pm.label("rid_dim"),
            func.sum(model_project.Project.amount_expected).label("expected"),
            func.sum(model_project.Project.amount_order).label("order"),
        )
        .select_from(model_project.Project)
        .where(*_get_filter(target))
        .group_by(model_project.Project.rid_users_pm)
        .order_by(model_project.Project.rid_users_pm)
    )
    _insert_summary_total(db, summary)
    # fmt: on


def _create_summaries_pl_total(
    db: Session,
    target: schema_summary.SummaryCreate,
) -> None:
    # fmt: off
    summary = (
        select(
            func.date("now", "localtime").label("date_snap"),
            literal(model_summary.TypeSummary.USER_PL.value).label("type"),
            model_project.Project.rid_users_pl.label("rid_dim"),
            func.sum(model_project.Project.amount_expected).label("expected"),
            func.sum(model_project.Project.amount_order).label("order"),
        )
        .select_from(model_project.Project)
        .where(*_get_filter(target))
        .group_by(model_project.Project.rid_users_pl)
        .order_by(model_project.Project.rid_users_pl)
    )
    _insert_summary_total(db, summary)
    # fmt: on


def _create_summaries_company_count(
    db: Session,
    target: schema_summary.SummaryCreate,
) -> None:
    # fmt: off
    summary = (
        select(
            func.date("now", "localtime").label("date_snap"),
            literal(model_summary.TypeSummary.COMPANY.value).label("type"),
            model_company.Company.rid.label("rid_dim"),
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
        .where(*_get_filter(target))
        .group_by(model_company.Company.rid, model_project.Project.rank)
        .order_by(model_company.Company.rid, model_project.Project.rank)
    )
    _insert_summary_count(db, summary)
    # fmt: on


def _create_summaries_project_count(
    db: Session,
    target: schema_summary.SummaryCreate,
) -> None:
    # fmt: off
    summary = (
        select(
            func.date("now", "localtime").label("date_snap"),
            literal(model_summary.TypeSummary.PROJECT.value).label("type"),
            model_project_group.ProjectGroup.rid.label("rid_dim"),
            model_project.Project.rank.label("rank"),
            func.count(model_project_group.ProjectGroup.rid).label("count"),
        )
        .select_from(model_project.Project)
        .join(
            model_project_group.ProjectGroup,
            model_project.Project.rid_project_groups == model_project_group.ProjectGroup.rid,
        )
        .where(*_get_filter(target))
        .group_by(model_project_group.ProjectGroup.rid, model_project.Project.rank)
        .order_by(model_project_group.ProjectGroup.rid, model_project.Project.rank)
    )
    _insert_summary_count(db, summary)
    # fmt: on


def _create_summaries_pm_count(
    db: Session,
    target: schema_summary.SummaryCreate,
) -> None:
    # fmt: off
    summary = (
        select(
            func.date("now", "localtime").label("date_snap"),
            literal(model_summary.TypeSummary.USER_PM.value).label("type"),
            model_project.Project.rid_users_pm.label("rid_dim"),
            model_project.Project.rank.label("rank"),
            func.count(model_project.Project.rid_users_pm).label("count"),
        )
        .select_from(model_project.Project)
        .where(*_get_filter(target))
        .group_by(model_project.Project.rid_users_pm, model_project.Project.rank)
        .order_by(model_project.Project.rid_users_pm, model_project.Project.rank)
    )
    _insert_summary_count(db, summary)
    # fmt: on


def _create_summaries_pl_count(
    db: Session,
    target: schema_summary.SummaryCreate,
) -> None:
    # fmt: off
    summary = (
        select(
            func.date("now", "localtime").label("date_snap"),
            literal(model_summary.TypeSummary.USER_PL.value).label("type"),
            model_project.Project.rid_users_pl.label("rid_dim"),
            model_project.Project.rank.label("rank"),
            func.count(model_project.Project.rid_users_pl).label("count"),
        )
        .select_from(model_project.Project)
        .where(*_get_filter(target))
        .group_by(model_project.Project.rid_users_pl, model_project.Project.rank)
        .order_by(model_project.Project.rid_users_pl, model_project.Project.rank)
    )
    _insert_summary_count(db, summary)
    # fmt: on


def _get_filter(target: schema_summary.SummaryCreate):
    str_snapshot_date = (target.date_snap or "").strip()
    has_target_date = bool(str_snapshot_date)

    where_clauses = [
        model_project.Project.is_deleted.is_(False),
    ]

    if has_target_date:
        where_clauses.append(
            cast(model_project.Project.updated_at, Date)
            <= func.date(literal(str_snapshot_date))
        )
    return where_clauses


def _insert_summary_total(db: Session, summary: select) -> None:
    stmt = insert(model_summary.SummaryTotal).from_select(
        ["date_snap", "type", "rid_dim", "expected", "order"],
        summary,
    )
    db.execute(stmt)


def _insert_summary_count(db: Session, summary: select) -> None:
    stmt = insert(model_summary.SummaryCount).from_select(
        ["date_snap", "type", "rid_dim", "rank", "count"],
        summary,
    )
    db.execute(stmt)
