from pydantic import BaseModel


class User(BaseModel):
    rid: int
    eid: str
    username: str
    name: str
    company: str
    post: int
    contract: int
    price: int

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    eid: str
    username: str
    password: str
    name: str
    company: str
    post: int
    contract: int
    price: int
    is_admin: bool

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    rid: int
    eid: str
    username: str
    password: str
    name: str
    company: str
    post: int
    contract: int
    price: int
    is_admin: bool

    class Config:
        orm_mode = True
