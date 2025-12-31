from typing import List

from app.models import target as model_target
from app.schemas import target as schema_target
from sqlalchemy.orm import Session


def get_targets(db: Session) -> List[schema_target.Target]:
    # fmt: off
    query = db.query(
        model_target.Target
    )\
    .filter(model_target.Target.is_deleted == 0)\
    .order_by(model_target.Target.rid)
    # fmt: on
    return query.all()


def create_target(
    db: Session, target: schema_target.TargetCreate
) -> schema_target.Target:
    # fmt: off
    obj_target = model_target.Target(
        year=target.year,
        quarter1=target.quarter1,
        quarter2=target.quarter2,
        quarter3=target.quarter3,
        quarter4=target.quarter4,
    )
    # fmt: on

    db.add(obj_target)
    db.commit()
    db.refresh(obj_target)
    return obj_target


def update_target(
    db: Session, target: schema_target.TargetUpdate
) -> schema_target.Target:
    # fmt: off
    obj_target = db.query(
        model_target.Target
    )\
    .filter(model_target.Target.rid == target.rid)\
    .first()

    obj_target.year    = target.year
    obj_target.quarter1 = target.quarter1
    obj_target.quarter2 = target.quarter2
    obj_target.quarter3 = target.quarter3
    obj_target.quarter4 = target.quarter4
    # fmt: on

    db.commit()
    db.refresh(obj_target)
    return obj_target


def delete_target(db: Session, rid: int) -> None:
    # fmt: off
    obj_target = db.query(
        model_target.Target
    )\
    .filter(model_target.Target.rid == rid)\
    .first()
    # fmt: on

    obj_target.is_deleted = 1
    db.commit()
