from datetime import datetime

from app.models import thread as model_thread
from app.schemas import base as schema_base
from app.schemas import user as schema_user


class Thread(schema_base.ORMBaseModel):
    rid: int
    depth: int
    user: schema_user.User
    state: model_thread.TypeThreadState
    note: str
    created_at: datetime


class ThreadReport(schema_base.ORMBaseModel):
    rid_projects: int
    threads: list[Thread]


class ThreadStatus(schema_base.ORMBaseModel):
    rid_projects: int
    count: int
    is_important: bool


class ThreadCreate(schema_base.ORMBaseModel):
    rid_projects: int
    rid_parent: int | None = None
    state: model_thread.TypeThreadState
    note: str


class ThreadUpdate(schema_base.ORMBaseModel):
    rid: int
    state: model_thread.TypeThreadState
    note: str
