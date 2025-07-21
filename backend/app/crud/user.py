from typing import List

from app.models import user as model_user
from app.schemas import user as schema_user
from sqlalchemy.orm import Session


def get_users(db: Session) -> List[model_user.User]:
    # fmt: off
    query = (
        db.query(model_user.User)
        .filter(not model_user.User.is_deleted)
        .order_by(model_user.User.rid)
    )
    # fmt: on
    return query.all()


def create_user(db: Session, target: schema_user.UserCreate) -> model_user.User:
    # fmt: off
    obj_user = model_user.User(
        id=target.eid,
        user=target.username,
        password=target.password,
        name=target.name,
        company=target.company,
        post=target.post,
        contract=target.contract,
        price=target.price,
        is_admin=target.is_admin,
    )
    # fmt: on

    db.add(obj_user)
    db.commit()
    db.refresh(obj_user)
    return obj_user


def update_user(db: Session, target: schema_user.UserUpdate) -> model_user.User:
    # fmt: off
    obj_user = db.query(
        model_user.User
    )\
    .filter(model_user.User.rid == target.rid)\
    .first()

    obj_user.id       = target.id
    obj_user.user     = target.user
    obj_user.password = target.password
    obj_user.name     = target.name
    obj_user.company  = target.company
    obj_user.post     = target.post
    obj_user.contract = target.contract
    obj_user.price    = target.price
    obj_user.is_admin = target.is_admin
    # fmt: on

    db.commit()
    db.refresh(obj_user)
    return obj_user


def delete_user(db: Session, rid: int) -> None:
    # fmt: off
    obj_user = db.query(
        model_user.User
    )\
    .filter(model_user.User.rid == rid)\
    .first()
    # fmt: on

    obj_user.is_deleted = True
    db.commit()
