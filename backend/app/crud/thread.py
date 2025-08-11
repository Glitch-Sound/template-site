from typing import List

from app.models import thread as model_thread
from app.schemas import thread as schema_thread
from app.schemas import user as schema_user
from sqlalchemy import and_, func, literal, select
from sqlalchemy.orm import Session, joinedload


def get_threads_by_rid(db: Session, rid_projects: int) -> List[model_thread.Thread]:
    t = model_thread.Thread.__table__

    def cat(a, b):
        return a.op("||")(b)

    # fmt: off
    roots = (
        select(
            t.c.rid.label("rid"),
            t.c.rid_parent.label("rid_parent"),
            func.printf('%020d', t.c.rid).label("sort_path"),
            literal(0).label("depth"),
        )
        .where(
            and_(
                t.c.rid_projects == rid_projects,
                t.c.is_deleted == 0,
                t.c.rid_parent.is_(None),
            )
        )
    )

    tree = roots.cte("tree", recursive=True)

    children = (
        select(
            t.c.rid,
            t.c.rid_parent,
            cat(cat(tree.c.sort_path, literal('.')),
                func.printf('%020d', t.c.rid)
            ).label("sort_path"),
            (tree.c.depth + 1).label("depth"),
        )
        .where(
            and_(
                t.c.is_deleted == 0,
                t.c.rid_projects == rid_projects,
                t.c.rid_parent == tree.c.rid,
            )
        )
    )

    tree = tree.union_all(children)

    rows = (
        db.query(model_thread.Thread, tree.c.depth)
          .join(tree, model_thread.Thread.rid == tree.c.rid)
          .options(joinedload(model_thread.Thread.user))
          .order_by(tree.c.sort_path.asc(), model_thread.Thread.rid.asc())
          .all()
    )
    # fmt: off

    result: List[model_thread.Thread] = []
    for obj, depth in rows:
        setattr(obj, "depth", int(depth))
        result.append(obj)
    return result


def create_thread(
    db: Session,
    target: schema_thread.ThreadCreate,
    current_user: schema_user.User,
) -> model_thread.Thread:
    print(target)

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

    obj_thread.depth = 0
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

    obj_thread.depth = 0
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
