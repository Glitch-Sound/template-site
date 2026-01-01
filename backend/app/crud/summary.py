from datetime import datetime

from app.models import project as model_project
from app.models import project_group as model_project_group
from app.models import summary as model_summary
from app.schemas import summary as schema_summary
from pytz import timezone
from sqlalchemy import Date, cast, func, literal, select
from sqlalchemy.orm import Session

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
