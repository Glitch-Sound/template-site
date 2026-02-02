from datetime import date
from typing import List

from app.models import company as model_company
from app.models import project as model_project
from app.models import project_group as model_project_group
from app.models import project_number as model_project_number
from app.models import user as model_user
from app.schemas import project as schema_project
from app.schemas import user as schema_user
from sqlalchemy import Integer, and_, cast, func, or_
from sqlalchemy.orm import Session, joinedload


def get_project_groups(db: Session) -> List[schema_project.ProjectGroup]:
    # fmt: off
    query = db.query(
        model_project_group.ProjectGroup
    )\
    .filter(model_project_group.ProjectGroup.is_deleted == 0)\
    .order_by(model_project_group.ProjectGroup.rid_companies, model_project_group.ProjectGroup.rid)
    # fmt: on
    return query.all()


def create_project_group(
    db: Session, target: schema_project.ProjectGroupCreate
) -> schema_project.ProjectGroup:
    # fmt: off
    obj_project_group = model_project_group.ProjectGroup(
        rid_companies=target.rid_companies,
        name=target.name,
        detail=target.detail,
    )
    # fmt: on

    db.add(obj_project_group)
    db.commit()
    db.refresh(obj_project_group)
    return obj_project_group


def update_project_group(
    db: Session, target: schema_project.ProjectGroupUpdate
) -> schema_project.ProjectGroup:
    # fmt: off
    obj_project_group = db.query(
        model_project_group.ProjectGroup
    )\
    .filter(model_project_group.ProjectGroup.rid == target.rid)\
    .first()

    obj_project_group.rid_companies = target.rid_companies
    obj_project_group.name          = target.name
    obj_project_group.detail        = target.detail
    # fmt: on

    db.commit()
    db.refresh(obj_project_group)
    return obj_project_group


def delete_project_group(db: Session, rid: int) -> None:
    # fmt: off
    obj_project_group = db.query(
        model_project_group.ProjectGroup
    )\
    .filter(model_project_group.ProjectGroup.rid == rid)\
    .first()
    # fmt: on

    obj_project_group.is_deleted = 1
    db.commit()


def get_project_numbers(db: Session, rid: int) -> List[schema_project.ProjectNumber]:
    # fmt: off
    query = db.query(
        model_project_number.ProjectNumber
    )\
    .filter(
        and_(
            model_project_number.ProjectNumber.is_deleted == 0,
            model_project_number.ProjectNumber.rid_projects == rid
        )
    )\
    .order_by(model_project_number.ProjectNumber.rid)
    # fmt: on
    return query.all()


def create_project_number(
    db: Session, target: schema_project.ProjectNumberCreate
) -> schema_project.ProjectNumber:
    # fmt: off
    obj_project_number = model_project_number.ProjectNumber(
        rid_projects=target.rid_projects,
        type=target.type,
        number=target.number,
        note=target.note,
        date_start=target.date_start,
        date_end=target.date_end
    )
    # fmt: on

    db.add(obj_project_number)
    db.commit()
    db.refresh(obj_project_number)
    return obj_project_number


def update_project_number(
    db: Session, target: schema_project.ProjectNumberUpdate
) -> schema_project.ProjectNumber:
    # fmt: off
    obj_project_number = db.query(
        model_project_number.ProjectNumber
    )\
    .filter(model_project_number.ProjectNumber.rid == target.rid)\
    .first()

    obj_project_number.rid_projects = target.rid_projects
    obj_project_number.type         = target.type
    obj_project_number.number       = target.number
    obj_project_number.note         = target.note
    obj_project_number.date_start   = target.date_start
    obj_project_number.date_end     = target.date_end
    # fmt: on

    db.commit()
    db.refresh(obj_project_number)
    return obj_project_number


def delete_project_number(db: Session, rid: int) -> None:
    # fmt: off
    obj_project_number = db.query(
        model_project_number.ProjectNumber
    )\
    .filter(model_project_number.ProjectNumber.rid == rid)\
    .first()
    # fmt: on

    obj_project_number.is_deleted = 1
    db.commit()


def get_project_condition(db: Session) -> schema_project.SearchCondition:
    # fmt: off
    year_expr    = cast(func.strftime('%Y', model_project.Project.date_end), Integer)
    month_expr   = cast(func.strftime('%m', model_project.Project.date_end), Integer)
    quarter_expr = cast((month_expr + 2) / 3.0, Integer)

    query_target = db.query(
        year_expr.label('year') * 10 + quarter_expr.label('quarter'),
    )\
    .filter(
        and_(
            model_project.Project.date_end.isnot(None),
            model_project.Project.date_end != "",
            model_project.Project.is_deleted == 0,
        )
    )\
    .distinct()\
    .order_by(year_expr.asc(), quarter_expr.asc())
    targets = [int(x[0]) for x in query_target.all()]
    # fmt: on

    # fmt: off
    query_pm = db.query(
        model_project.Project.rid_users_pm
    )\
    .filter(
        and_(
            model_project.Project.rid_users_pm.isnot(None),
            model_project.Project.is_deleted == 0,
        )
    )\
    .distinct()\
    .order_by(model_project.Project.rid_users_pm.asc())
    rid_users_pm = [int(x[0]) for x in query_pm.all()]
    # fmt: on

    # fmt: off
    query_pl = db.query(
        model_project.Project.rid_users_pl
    )\
    .filter(
        and_(
            model_project.Project.rid_users_pl.isnot(None),
            model_project.Project.is_deleted == 0,
        )
    )\
    .distinct()\
    .order_by(model_project.Project.rid_users_pl.asc())
    rid_users_pl = [int(x[0]) for x in query_pl.all()]
    # fmt: on

    # fmt: off
    query_companies = db.query(
        model_company.Company.rid
    )\
    .filter(
        and_(
            model_company.Company.is_deleted == 0,
        )
    )\
    .distinct()\
    .order_by(model_company.Company.rid.asc())
    rid_companies = [int(x[0]) for x in query_companies.all()]
    # fmt: on

    ranks = [
        rank.value
        for rank in model_project.TypeRank
        if rank != model_project.TypeRank.NONE
    ]

    return schema_project.SearchCondition(
        target=targets,
        rid_companies=rid_companies,
        rid_users_pm=rid_users_pm,
        rid_users_pl=rid_users_pl,
        ranks=ranks,
        is_none_pre_approval=0,
        is_none_number_m=0,
        is_none_number_s=0,
        is_none_number_o=0,
    )


def get_project_targets(db: Session) -> schema_project.TargetQuarter:
    # fmt: off
    year_expr    = cast(func.strftime('%Y', model_project.Project.date_end), Integer)
    month_expr   = cast(func.strftime('%m', model_project.Project.date_end), Integer)
    quarter_expr = cast((month_expr + 2) / 3.0, Integer)

    query_target = db.query(
        year_expr.label('year'),
        quarter_expr.label('quarter'),
    )\
    .filter(
        and_(
            model_project.Project.date_end.isnot(None),
            model_project.Project.date_end != "",
            model_project.Project.is_deleted == 0,
        )
    )\
    .distinct()\
    .order_by(year_expr.asc(), quarter_expr.asc())
    rows_target = query_target.all()
    # fmt: on

    targets = [
        schema_project.TargetQuarter(year=int(r.year), quarter=int(r.quarter))
        for r in rows_target
    ]

    return targets


def get_project_users(db: Session) -> schema_user.User:
    # fmt: off
    query_pm = db.query(
        model_project.Project.rid_users_pm.label("rid")
    )\
    .filter(
        and_(
            model_project.Project.rid_users_pm.isnot(None),
            model_project.Project.is_deleted == 0,
        )
    )

    query_pl = db.query(
        model_project.Project.rid_users_pl.label("rid")
    )\
    .filter(
        and_(
            model_project.Project.rid_users_pl.isnot(None),
            model_project.Project.is_deleted == 0,
        )
    )
    # fmt: on

    rids_sq = query_pm.union(query_pl).subquery("rids")

    # fmt: off
    q_users = (
        db.query(
            model_user.User
        )
        .join(rids_sq, model_user.User.rid == rids_sq.c.rid)
        .order_by(model_user.User.rid)
    )
    # fmt: on

    q_users = q_users.filter(~model_user.User.is_deleted)

    return q_users.all()


def get_projects(
    db: Session, condition: schema_project.SearchCondition
) -> list[schema_project.ProjectList]:
    child_preds = [model_project.Project.is_deleted == 0]

    if condition.target:
        child_preds.append(
            or_(
                model_project.Project.target_quarter.in_(condition.target),
                model_project.Project.date_end.is_(None),
                model_project.Project.date_end == "",
            )
        )

    if condition.rid_users_pm:
        child_preds.append(
            model_project.Project.rid_users_pm.in_(condition.rid_users_pm)
        )

    if condition.rid_users_pl:
        child_preds.append(
            model_project.Project.rid_users_pl.in_(condition.rid_users_pl)
        )

    if condition.ranks:
        child_preds.append(model_project.Project.rank.in_(condition.ranks))

    if condition.is_none_pre_approval:
        child_preds.append(
            or_(
                model_project.Project.pre_approval.is_(None),
                model_project.Project.pre_approval == "",
            )
        )

    if condition.is_none_number_m:
        child_preds.append(model_project.Project.number_m == 0)

    if condition.is_none_number_s:
        child_preds.append(model_project.Project.number_s == 0)

    if condition.is_none_number_o:
        child_preds.append(model_project.Project.number_o == 0)

    group_preds = [
        model_project_group.ProjectGroup.is_deleted == 0,
        model_project_group.ProjectGroup.projects.any(and_(*child_preds)),
    ]

    if condition.rid_companies:
        group_preds.append(
            model_project_group.ProjectGroup.rid_companies.in_(condition.rid_companies)
        )

    query = (
        db.query(model_project_group.ProjectGroup)
        .options(
            joinedload(
                model_project_group.ProjectGroup.projects.and_(and_(*child_preds))
            ).joinedload(model_project.Project.project_numbers)
        )
        .filter(and_(*group_preds))
        .order_by(
            model_project_group.ProjectGroup.rid_companies,
            model_project_group.ProjectGroup.rid,
        )
    )

    return query.all()


def get_project_report(
    db: Session, rid_users: int | None
) -> list[schema_project.ProjectList]:
    today = date.today().isoformat()
    child_preds = [
        model_project.Project.is_deleted == 0,
        model_project.Project.date_start <= today,
        model_project.Project.date_end >= today,
    ]
    if rid_users is not None:
        child_preds.append(model_project.Project.rid_users_pl == rid_users)

    group_preds = [
        model_project_group.ProjectGroup.is_deleted == 0,
        model_project_group.ProjectGroup.projects.any(and_(*child_preds)),
    ]

    query = (
        db.query(model_project_group.ProjectGroup)
        .options(
            joinedload(
                model_project_group.ProjectGroup.projects.and_(and_(*child_preds))
            ).joinedload(model_project.Project.project_numbers)
        )
        .filter(and_(*group_preds))
        .order_by(
            model_project_group.ProjectGroup.rid_companies,
            model_project_group.ProjectGroup.rid,
        )
    )

    return query.all()


def _get_target(date_end: str) -> int:
    if not date_end:
        return 0
    date_end = date.fromisoformat(date_end)
    return date_end.year * 10 + (date_end.month + 2) // 3


def create_project(
    db: Session, target: schema_project.ProjectCreate
) -> schema_project.Project:
    # fmt: off
    obj_project = model_project.Project(
        rid_project_groups=target.rid_project_groups,
        rid_users_pm=target.rid_users_pm,
        rid_users_pl=target.rid_users_pl,
        rank=target.rank,
        pre_approval=target.pre_approval,
        name=target.name,
        number_parent=target.number_parent,
        amount_expected=target.amount_expected,
        amount_order=target.amount_order,
        date_start=target.date_start,
        date_delivery=target.date_delivery,
        date_end=target.date_end,
        target_quarter=_get_target(target.date_end)
    )
    # fmt: on

    db.add(obj_project)
    db.commit()
    db.refresh(obj_project)
    return obj_project


def update_project(
    db: Session, target: schema_project.ProjectUpdate
) -> schema_project.Project:
    # fmt: off
    obj_project = db.query(
        model_project.Project
    )\
    .filter(model_project.Project.rid == target.rid)\
    .first()

    obj_project.rid_project_groups = target.rid_project_groups
    obj_project.rid_users_pm       = target.rid_users_pm
    obj_project.rid_users_pl       = target.rid_users_pl
    obj_project.rank               = target.rank
    obj_project.pre_approval       = target.pre_approval
    obj_project.name               = target.name
    obj_project.number_parent      = target.number_parent
    obj_project.amount_expected    = target.amount_expected
    obj_project.amount_order       = target.amount_order
    obj_project.date_start         = target.date_start
    obj_project.date_delivery      = target.date_delivery
    obj_project.date_end           = target.date_end
    obj_project.target_quarter     = _get_target(target.date_end)
    # fmt: on

    db.commit()
    db.refresh(obj_project)
    return obj_project


def delete_project(db: Session, rid: int) -> None:
    # fmt: off
    obj_project = db.query(
        model_project.Project
    )\
    .filter(model_project.Project.rid == rid)\
    .first()
    # fmt: on

    obj_project.is_deleted = 1
    db.commit()
