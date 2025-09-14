from app.models import user as model_user
from app.schemas import base as schema_base


class User(schema_base.ORMBaseModel):
    rid: int
    eid: str
    username: str
    name: str
    company: str
    post: model_user.TypePost
    contract: model_user.TypeContract
    is_admin: bool


class UserCreate(schema_base.ORMBaseModel):
    eid: str
    username: str
    password: str
    name: str
    company: str
    post: model_user.TypePost
    contract: model_user.TypeContract
    is_admin: bool


class UserUpdate(schema_base.ORMBaseModel):
    rid: int
    eid: str
    username: str
    password: str
    name: str
    company: str
    post: model_user.TypePost
    contract: model_user.TypeContract
    is_admin: bool
