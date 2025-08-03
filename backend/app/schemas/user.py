from enum import IntEnum

from pydantic import BaseModel


# fmt: off
class TypePost(IntEnum):
    NONE = 0
    K    = 1
    C    = 2
    L    = 3
    T    = 4
    BP   = 5


class TypeContract(IntEnum):
    NONE      = 0
    PROPER    = 1
    TEMP      = 2
    CONSIGN_C = 3
    CONSIGN_M = 4
# fmt: on


class User(BaseModel):
    rid: int
    eid: str
    username: str
    name: str
    company: str
    post: TypePost
    contract: TypeContract
    price: int
    is_admin: bool

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    eid: str
    username: str
    password: str
    name: str
    company: str
    post: TypePost
    contract: TypeContract
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
    post: TypePost
    contract: TypeContract
    price: int
    is_admin: bool

    class Config:
        orm_mode = True
