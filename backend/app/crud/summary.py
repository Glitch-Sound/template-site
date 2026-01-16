from calendar import monthrange
from datetime import date, datetime, timedelta

from app.models import company as model_company
from app.models import project as model_project
from app.models import project_group as model_project_group
from app.models import summary as model_summary
from app.models import user as model_user
from app.schemas import project as schema_project
from app.schemas import summary as schema_summary
from pytz import timezone
from sqlalchemy import Date, and_, cast, func, literal, or_, select
from sqlalchemy.orm import Session, aliased

JST = timezone("Asia/Tokyo")


def get_summaries_amount(
    db: Session,
    year: int,
) -> list[schema_summary.SummaryAmount]:
    # fmt: off
    query = db.query(
        model_summary.SummaryAmount
    )\
    .filter(
        model_summary.SummaryAmount.date_snap.startswith(f"{year}-")
    )\
    .order_by(model_summary.SummaryAmount.rid)
    # fmt: on

    return query.all()


def get_summaries_amount_latest(
    db: Session,
) -> schema_summary.SummaryAmount:
    latest = select(func.max(model_summary.SummaryAmount.date_snap)).scalar_subquery()

    # fmt: off
    query = db.query(
        model_summary.SummaryAmount
    )\
    .filter(
        model_summary.SummaryAmount.date_snap == latest
    )\
    .order_by(model_summary.SummaryAmount.rid)
    # fmt: on

    return query.all()


def get_summaries_company(
    db: Session,
    year: int,
) -> list[schema_summary.SummaryCompany]:
    # fmt: off
    query = db.query(
        model_summary.SummaryCompany
    )\
    .filter(
        model_summary.SummaryCompany.date_snap.startswith(f"{year}-")
    )\
    .order_by(model_summary.SummaryCompany.rid_companies, model_summary.SummaryCompany.rid)
    # fmt: on

    return query.all()


def get_summaries_company_latest(
    db: Session,
) -> schema_summary.SummaryCompany:
    latest = select(func.max(model_summary.SummaryCompany.date_snap)).scalar_subquery()

    # fmt: off
    query = db.query(
        model_summary.SummaryCompany
    )\
    .filter(
        model_summary.SummaryCompany.date_snap == latest
    )\
    .order_by(model_summary.SummaryCompany.rid_companies, model_summary.SummaryCompany.rid)
    # fmt: on

    return query.all()


def get_summaries_sankey(
    db: Session,
) -> schema_summary.SankeySummary:
    year = datetime.now(JST).year
    quarter_start = year * 10 + 1
    quarter_end = year * 10 + 4
    target_ranks = [model_project.TypeRank.A.value, model_project.TypeRank.B.value]

    base_filters = [
        model_project.Project.is_deleted.is_(False),
        model_project.Project.rank.in_(target_ranks),
        model_project.Project.target_quarter >= quarter_start,
        model_project.Project.target_quarter <= quarter_end,
        model_project_group.ProjectGroup.is_deleted.is_(False),
        model_company.Company.is_deleted.is_(False),
    ]

    # fmt: off
    total_amount = db.query(
        func.sum(model_project.Project.amount_order)
    )\
    .join(
        model_project_group.ProjectGroup,
        model_project.Project.rid_project_groups == model_project_group.ProjectGroup.rid,
    )\
    .join(
        model_company.Company,
        model_project_group.ProjectGroup.rid_companies == model_company.Company.rid,
    )\
    .filter(*base_filters)\
    .scalar() or 0
    # fmt: on

    # fmt: off
    company_rows = db.query(
        model_project_group.ProjectGroup.rid_companies.label("company_rid"),
        model_company.Company.name.label("company_name"),
        func.sum(model_project.Project.amount_order).label("amount"),
    )\
    .join(
        model_project_group.ProjectGroup,
        model_project.Project.rid_project_groups == model_project_group.ProjectGroup.rid,
    )\
    .join(
        model_company.Company,
        model_project_group.ProjectGroup.rid_companies == model_company.Company.rid,
    )\
    .filter(*base_filters)\
    .group_by(
        model_project_group.ProjectGroup.rid_companies,
        model_company.Company.name,
    )\
    .order_by(func.sum(model_project.Project.amount_order).desc())\
    .all()
    # fmt: on

    pm_user = aliased(model_user.User)
    pm_rid_expr = func.coalesce(model_project.Project.rid_users_pm, literal(0))
    pm_name_expr = func.coalesce(pm_user.name, literal("Unknown"))

    # fmt: off
    company_pm_rows = db.query(
        model_project_group.ProjectGroup.rid_companies.label("company_rid"),
        model_company.Company.name.label("company_name"),
        pm_rid_expr.label("pm_rid"),
        pm_name_expr.label("pm_name"),
        func.sum(model_project.Project.amount_order).label("amount"),
    )\
    .join(
        model_project_group.ProjectGroup,
        model_project.Project.rid_project_groups == model_project_group.ProjectGroup.rid,
    )\
    .join(
        model_company.Company,
        model_project_group.ProjectGroup.rid_companies == model_company.Company.rid,
    )\
    .outerjoin(
        pm_user,
        model_project.Project.rid_users_pm == pm_user.rid,
    )\
    .filter(*base_filters)\
    .group_by(
        model_project_group.ProjectGroup.rid_companies,
        model_company.Company.name,
        pm_rid_expr,
        pm_name_expr,
    )\
    .order_by(func.sum(model_project.Project.amount_order).desc())\
    .all()
    # fmt: on

    pm_user = aliased(model_user.User)
    pl_user = aliased(model_user.User)
    pm_rid_expr = func.coalesce(model_project.Project.rid_users_pm, literal(0))
    pm_name_expr = func.coalesce(pm_user.name, literal("Unknown"))
    pl_rid_expr = func.coalesce(model_project.Project.rid_users_pl, literal(0))
    pl_name_expr = func.coalesce(pl_user.name, literal("Unknown"))

    # fmt: off
    pm_pl_rows = db.query(
        pm_rid_expr.label("pm_rid"),
        pm_name_expr.label("pm_name"),
        pl_rid_expr.label("pl_rid"),
        pl_name_expr.label("pl_name"),
        func.sum(model_project.Project.amount_order).label("amount"),
    )\
    .join(
        model_project_group.ProjectGroup,
        model_project.Project.rid_project_groups == model_project_group.ProjectGroup.rid,
    )\
    .join(
        model_company.Company,
        model_project_group.ProjectGroup.rid_companies == model_company.Company.rid,
    )\
    .outerjoin(
        pm_user,
        model_project.Project.rid_users_pm == pm_user.rid,
    )\
    .outerjoin(
        pl_user,
        model_project.Project.rid_users_pl == pl_user.rid,
    )\
    .filter(*base_filters)\
    .group_by(
        pm_rid_expr,
        pm_name_expr,
        pl_rid_expr,
        pl_name_expr,
    )\
    .order_by(func.sum(model_project.Project.amount_order).desc())\
    .all()
    # fmt: on

    companies = [
        schema_summary.SankeyCompany(
            rid=row.company_rid,
            name=row.company_name,
            amount=row.amount or 0,
        )
        for row in company_rows
        if row.company_rid is not None
    ]

    company_pm = [
        schema_summary.SankeyCompanyPm(
            company_rid=row.company_rid,
            company_name=row.company_name,
            pm_rid=row.pm_rid or 0,
            pm_name=row.pm_name or "Unknown",
            amount=row.amount or 0,
        )
        for row in company_pm_rows
        if row.company_rid is not None
    ]

    pm_pl = [
        schema_summary.SankeyPmPl(
            pm_rid=row.pm_rid or 0,
            pm_name=row.pm_name or "Unknown",
            pl_rid=row.pl_rid or 0,
            pl_name=row.pl_name or "Unknown",
            amount=row.amount or 0,
        )
        for row in pm_pl_rows
    ]

    return schema_summary.SankeySummary(
        year=year,
        total_amount=total_amount,
        companies=companies,
        company_pm=company_pm,
        pm_pl=pm_pl,
    )


# ---------------------------------------------------------------------------


def create_summaries(
    db: Session,
    target: schema_summary.SummaryCreate,
) -> None:
    target_date = (target.date_snap or "").strip()
    snapshot_date = target_date or _today_jst()
    filters = _get_filter(target_date)
    try:
        _clear_summaries(db, snapshot_date)
        _create_summaries_amount(db, filters, snapshot_date)
        _create_summaries_company(db, filters, snapshot_date)
        db.commit()

    except Exception:
        db.rollback()
        raise


def _clear_summaries(db: Session, snapshot_date: str) -> None:
    db.query(model_summary.SummaryAmount).filter(
        model_summary.SummaryAmount.date_snap == snapshot_date
    ).delete(synchronize_session=False)
    db.query(model_summary.SummaryCompany).filter(
        model_summary.SummaryCompany.date_snap == snapshot_date
    ).delete(synchronize_session=False)


def _create_summaries_amount(
    db: Session,
    filters: list,
    snapshot_date: str,
) -> None:
    try:
        year = int(snapshot_date.split("-")[0])
    except (ValueError, AttributeError, IndexError):
        return

    quarter_ids = [year * 10 + quarter for quarter in range(1, 5)]

    # fmt: off
    rows = db.query(
        model_project.Project.rank,
        model_project.Project.target_quarter,
        func.sum(model_project.Project.amount_expected).label("sum_expected"),
        func.sum(model_project.Project.amount_order).label("sum_order"),
    )\
    .filter(*filters)\
    .filter(model_project.Project.target_quarter.in_(quarter_ids))\
    .filter(model_project.Project.rank != model_project.TypeRank.NONE.value)\
    .group_by(model_project.Project.rank, model_project.Project.target_quarter)\
    .all()
    # fmt: on

    totals: dict[int, dict[str, int]] = {}

    for rank in model_project.TypeRank:
        if rank == model_project.TypeRank.NONE:
            continue
        totals[rank.value] = {
            "quarter1_expected": 0,
            "quarter1_order": 0,
            "quarter2_expected": 0,
            "quarter2_order": 0,
            "quarter3_expected": 0,
            "quarter3_order": 0,
            "quarter4_expected": 0,
            "quarter4_order": 0,
        }

    for row in rows:
        quarter = row.target_quarter - year * 10
        if quarter not in (1, 2, 3, 4):
            continue
        if row.rank == model_project.TypeRank.NONE.value:
            continue
        target = totals.setdefault(
            row.rank,
            {
                "quarter1_expected": 0,
                "quarter1_order": 0,
                "quarter2_expected": 0,
                "quarter2_order": 0,
                "quarter3_expected": 0,
                "quarter3_order": 0,
                "quarter4_expected": 0,
                "quarter4_order": 0,
            },
        )
        expected = row.sum_expected or 0
        ordered = row.sum_order or 0
        target[f"quarter{quarter}_expected"] += expected
        target[f"quarter{quarter}_order"] += ordered

    summaries: list[model_summary.SummaryAmount] = []
    for rank, data in totals.items():
        quarter1_expected = data["quarter1_expected"]
        quarter2_expected = data["quarter2_expected"]
        quarter3_expected = data["quarter3_expected"]
        quarter4_expected = data["quarter4_expected"]
        quarter1_order = data["quarter1_order"]
        quarter2_order = data["quarter2_order"]
        quarter3_order = data["quarter3_order"]
        quarter4_order = data["quarter4_order"]
        half_first_expected = quarter1_expected + quarter2_expected
        half_second_expected = quarter3_expected + quarter4_expected
        half_first_order = quarter1_order + quarter2_order
        half_second_order = quarter3_order + quarter4_order
        all_expected = half_first_expected + half_second_expected
        all_order = half_first_order + half_second_order

        summaries.append(
            model_summary.SummaryAmount(
                date_snap=snapshot_date,
                rank=rank,
                quarter1_expected=quarter1_expected,
                quarter1_order=quarter1_order,
                quarter2_expected=quarter2_expected,
                quarter2_order=quarter2_order,
                quarter3_expected=quarter3_expected,
                quarter3_order=quarter3_order,
                quarter4_expected=quarter4_expected,
                quarter4_order=quarter4_order,
                half_first_expected=half_first_expected,
                half_first_order=half_first_order,
                half_second_expected=half_second_expected,
                half_second_order=half_second_order,
                all_expected=all_expected,
                all_order=all_order,
            )
        )

    if summaries:
        db.add_all(summaries)


def _create_summaries_company(
    db: Session,
    filters: list,
    snapshot_date: str,
) -> None:
    try:
        year = int(snapshot_date.split("-")[0])
    except (ValueError, AttributeError, IndexError):
        return

    quarter_ids = [year * 10 + quarter for quarter in range(1, 5)]

    # fmt: off
    rows = db.query(
        model_project_group.ProjectGroup.rid_companies.label("rid_companies"),
        model_project.Project.rank,
        model_project.Project.target_quarter,
        func.sum(model_project.Project.amount_expected).label("sum_expected"),
        func.sum(model_project.Project.amount_order).label("sum_order"),
    )\
    .join(
        model_project_group.ProjectGroup,
        model_project.Project.rid_project_groups == model_project_group.ProjectGroup.rid,
    )\
    .filter(*filters)\
    .filter(model_project_group.ProjectGroup.is_deleted.is_(False))\
    .filter(model_project.Project.target_quarter.in_(quarter_ids))\
    .filter(model_project.Project.rank != model_project.TypeRank.NONE.value)\
    .group_by(
        model_project_group.ProjectGroup.rid_companies,
        model_project.Project.rank,
        model_project.Project.target_quarter,
    )\
    .all()
    # fmt: on

    companies = {row.rid_companies for row in rows if row.rid_companies is not None}
    totals: dict[tuple[int, int], dict[str, int]] = {}

    for rid_companies in companies:
        for rank in model_project.TypeRank:
            if rank == model_project.TypeRank.NONE:
                continue
            totals[(rid_companies, rank.value)] = {
                "quarter1_expected": 0,
                "quarter1_order": 0,
                "quarter2_expected": 0,
                "quarter2_order": 0,
                "quarter3_expected": 0,
                "quarter3_order": 0,
                "quarter4_expected": 0,
                "quarter4_order": 0,
            }

    for row in rows:
        if row.rid_companies is None:
            continue
        quarter = row.target_quarter - year * 10
        if quarter not in (1, 2, 3, 4):
            continue
        if row.rank == model_project.TypeRank.NONE.value:
            continue
        target = totals.setdefault(
            (row.rid_companies, row.rank),
            {
                "quarter1_expected": 0,
                "quarter1_order": 0,
                "quarter2_expected": 0,
                "quarter2_order": 0,
                "quarter3_expected": 0,
                "quarter3_order": 0,
                "quarter4_expected": 0,
                "quarter4_order": 0,
            },
        )
        expected = row.sum_expected or 0
        ordered = row.sum_order or 0
        target[f"quarter{quarter}_expected"] += expected
        target[f"quarter{quarter}_order"] += ordered

    summaries: list[model_summary.SummaryCompany] = []
    for (rid_companies, rank), data in totals.items():
        quarter1_expected = data["quarter1_expected"]
        quarter2_expected = data["quarter2_expected"]
        quarter3_expected = data["quarter3_expected"]
        quarter4_expected = data["quarter4_expected"]
        quarter1_order = data["quarter1_order"]
        quarter2_order = data["quarter2_order"]
        quarter3_order = data["quarter3_order"]
        quarter4_order = data["quarter4_order"]
        half_first_expected = quarter1_expected + quarter2_expected
        half_second_expected = quarter3_expected + quarter4_expected
        half_first_order = quarter1_order + quarter2_order
        half_second_order = quarter3_order + quarter4_order
        all_expected = half_first_expected + half_second_expected
        all_order = half_first_order + half_second_order

        summaries.append(
            model_summary.SummaryCompany(
                date_snap=snapshot_date,
                rid_companies=rid_companies,
                rank=rank,
                quarter1_expected=quarter1_expected,
                quarter1_order=quarter1_order,
                quarter2_expected=quarter2_expected,
                quarter2_order=quarter2_order,
                quarter3_expected=quarter3_expected,
                quarter3_order=quarter3_order,
                quarter4_expected=quarter4_expected,
                quarter4_order=quarter4_order,
                half_first_expected=half_first_expected,
                half_first_order=half_first_order,
                half_second_expected=half_second_expected,
                half_second_order=half_second_order,
                all_expected=all_expected,
                all_order=all_order,
            )
        )

    if summaries:
        db.add_all(summaries)


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


def get_summaries_deadline(db: Session) -> list[schema_project.Project]:
    today = date.today()
    start = today.isoformat()
    end = (today + timedelta(days=14)).isoformat()

    # fmt: off
    query = db.query(
        model_project.Project
    )\
    .filter(
        model_project.Project.is_deleted == 0,
        _date_range_pred(model_project.Project.date_delivery, start, end),
    )\
    .order_by(model_project.Project.date_delivery.asc(), model_project.Project.rid.asc())
    # fmt: on

    return query.all()


def get_summaries_incomplete(db: Session) -> list[schema_project.Project]:
    today = date.today()
    start = today.isoformat()
    end = _add_months(today, 1).isoformat()

    # fmt: off
    query = db.query(
        model_project.Project
    )\
    .filter(
        model_project.Project.is_deleted == 0,
        _date_range_pred(model_project.Project.date_start, start, end),
        or_(
            model_project.Project.pre_approval.is_(None),
            model_project.Project.pre_approval == "",
        ),
    )\
    .order_by(model_project.Project.date_start.asc(), model_project.Project.rid.asc())
    # fmt: on

    return query.all()


def get_summaries_alert(db: Session) -> list[schema_project.Project]:
    today = date.today()
    start = today.isoformat()
    end = (today + timedelta(days=14)).isoformat()

    # fmt: off
    query = db.query(
        model_project.Project
    )\
    .filter(
        model_project.Project.is_deleted == 0,
        _date_range_pred(model_project.Project.date_start, start, end),
        or_(
            model_project.Project.number_s == 0,
            model_project.Project.number_o == 0,
        ),
    )\
    .order_by(model_project.Project.date_start.asc(), model_project.Project.rid.asc())
    # fmt: on

    return query.all()


def _add_months(source: date, months: int) -> date:
    month = source.month - 1 + months
    year = source.year + month // 12
    month = month % 12 + 1
    day = min(source.day, monthrange(year, month)[1])
    return date(year, month, day)


def _date_range_pred(column, start: str, end: str):
    return and_(
        column.isnot(None),
        column != "",
        column >= start,
        column <= end,
    )
