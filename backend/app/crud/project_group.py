from typing import List

from app.models import project_group as model_project_group
from app.schemas import project_group as schema_project_group
from sqlalchemy.orm import Session


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
    db: Session, target: schema_project_group.ProjectGroupCreate
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
    db: Session, target: schema_project_group.ProjectGroupUpdate
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
