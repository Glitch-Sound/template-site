from typing import List

from app.models import project as model_project
from app.models import project_group as model_project_group
from app.schemas import project as schema_project
from sqlalchemy import and_
from sqlalchemy.orm import Session, joinedload


def get_project_groups(db: Session) -> List[model_project_group.ProjectGroup]:
    # fmt: off
    query = db.query(
        model_project_group.ProjectGroup
    )\
    .filter(~model_project_group.ProjectGroup.is_deleted)\
    .order_by(model_project_group.ProjectGroup.rid)
    # fmt: on
    return query.all()


def create_project_group(
    db: Session, target: schema_project.ProjectGroupCreate
) -> model_project_group.ProjectGroup:
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
) -> model_project_group.ProjectGroup:
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

    obj_project_group.is_deleted = True
    db.commit()


def get_projects(db: Session) -> List[model_project.Project]:
    # fmt: off
    query = db.query(
        model_project.Project
    )\
    .filter(~model_project.Project.is_deleted)\
    .order_by(model_project.Project.rid)
    # fmt: on
    return query.all()


def create_project(
    db: Session, target: schema_project.ProjectCreate
) -> model_project.Project:
    # fmt: off
    obj_project = model_project.Project(
        rid_project_groups=target.rid_project_groups,
        rid_users_pm=target.rid_users_pm,
        rid_users_pl=target.rid_users_pl,
        rank=target.rank,
        title=target.title,
        amount_expected=target.amount_expected,
        amount_order=target.amount_order,
        date_start=target.date_start,
        date_delivery=target.date_delivery,
        date_end=target.date_end,
        karte_plan=target.karte_plan,
        karte_report=target.karte_report,
        checklist=target.checklist,
        no_parent=target.no_parent,
    )
    # fmt: on

    db.add(obj_project)
    db.commit()
    db.refresh(obj_project)
    return obj_project


def update_project(
    db: Session, target: schema_project.ProjectUpdate
) -> model_project.Project:
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
    obj_project.title              = target.title
    obj_project.amount_expected    = target.amount_expected
    obj_project.amount_order       = target.amount_order
    obj_project.date_start         = target.date_start
    obj_project.date_delivery      = target.date_delivery
    obj_project.date_end           = target.date_end
    obj_project.karte_plan         = target.karte_plan
    obj_project.karte_report       = target.karte_report
    obj_project.checklist          = target.checklist
    obj_project.no_parent          = target.no_parent
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

    obj_project.is_deleted = True
    db.commit()


def get_projects_all(db: Session) -> List[model_project_group.ProjectGroup]:
    # fmt: off
    query = db.query(
        model_project_group.ProjectGroup
    )\
    .options(
        joinedload(model_project_group.ProjectGroup.projects),
        joinedload(model_project_group.ProjectGroup.projects).joinedload(model_project.Project.project_numbers)
    )\
    .filter(
            and_(
                ~model_project_group.ProjectGroup.is_deleted,
                ~model_project.Project.is_deleted
            )
    )\
    .order_by(model_project_group.ProjectGroup.rid, model_project.Project.rid)
    # fmt: on
    return query.all()
