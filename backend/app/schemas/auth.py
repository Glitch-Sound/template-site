from app.schemas import base as schema_base


class Status(schema_base.ORMBaseModel):
    is_setup: bool


class Token(schema_base.ORMBaseModel):
    rid: int
    token_access: str
    token_refresh: str
    token_type: str = "bearer"


class Login(schema_base.ORMBaseModel):
    username: str
    password: str


class Refresh(schema_base.ORMBaseModel):
    token_refresh: str
