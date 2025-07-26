from pydantic import BaseModel


class Token(BaseModel):
    token_access: str
    token_refresh: str
    token_type: str = "bearer"


class Login(BaseModel):
    username: str
    password: str


class Refresh(BaseModel):
    token_refresh: str
