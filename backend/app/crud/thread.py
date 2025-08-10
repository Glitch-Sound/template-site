from typing import List

from app.models import thread as model_thread
from app.schemas import thread as schema_thread
from app.schemas import user as schema_user
from sqlalchemy import and_
from sqlalchemy.orm import Session


def get_threads_by_rid(db: Session, rid_projects: int) -> List[model_thread.Thread]:
    # fmt: off
    query = db.query(
        model_thread.Thread
    )\
    .filter(
        and_(
            model_thread.Thread.rid_projects == rid_projects,
            model_thread.Thread.is_deleted == 0
        )
    )\
    .order_by(
        model_thread.Thread.rid_parent.asc().nullsfirst(),
        model_thread.Thread.rid.asc()
    )
    # fmt: on
    return query.all()


def create_thread(
    db: Session,
    target: schema_thread.ThreadCreate,
    current_user: schema_user.User,
) -> model_thread.Thread:
    # fmt: off
    obj_thread = model_thread.Thread(
        rid_projects=target.rid_projects,
        rid_parent=target.rid_parent,
        rid_users=current_user.rid,
        state=target.state,
        note=target.note,
        is_deleted=0
    )
    # fmt: on

    db.add(obj_thread)
    db.commit()
    db.refresh(obj_thread)
    return obj_thread


def update_thread(
    db: Session, target: schema_thread.ThreadUpdate, current_user: schema_user.User
) -> model_thread.Thread:
    # fmt: off
    obj_thread = db.query(
        model_thread.Thread
    )\
    .filter(model_thread.Thread.rid == target.rid)\
    .first()

    obj_thread.rid_users = current_user.rid
    obj_thread.state     = target.state
    obj_thread.note      = target.note
    # fmt: on

    db.commit()
    db.refresh(obj_thread)
    return obj_thread


def delete_thread(db: Session, rid: int) -> None:
    # fmt: off
    obj_thread = db.query(
        model_thread.Thread
    )\
    .filter(model_thread.Thread.rid == rid)\
    .first()
    # fmt: on

    obj_thread.is_deleted = 1
    db.commit()
