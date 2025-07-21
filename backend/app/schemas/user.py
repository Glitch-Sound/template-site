from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    password: str


class User(UserBase):
    rid: int

    class Config:
        orm_mode = True
