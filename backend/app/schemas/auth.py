from pydantic import BaseModel


class Status(BaseModel):
    is_setup: bool


class Token(BaseModel):
    rid: int
    token_access: str
    token_refresh: str
    token_type: str = "bearer"


class Login(BaseModel):
    username: str
    password: str


class Refresh(BaseModel):
    token_refresh: str
