from datetime import datetime

from app.models import thread as model_thread
from app.schemas import user as schema_user
from pydantic import BaseModel


class Thread(BaseModel):
    rid: int
    depth: int
    user: schema_user.User
    state: model_thread.TypeThreadState
    note: str
    created_at: datetime

    class Config:
        orm_mode = True


class ThreadCreate(BaseModel):
    rid_projects: int
    rid_parent: int | None = None
    state: model_thread.TypeThreadState
    note: str

    class Config:
        orm_mode = True


class ThreadUpdate(BaseModel):
    rid: int
    state: model_thread.TypeThreadState
    note: str

    class Config:
        orm_mode = True
