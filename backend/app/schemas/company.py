from pydantic import BaseModel


class Company(BaseModel):
    rid: int
    name: str
    detail: str

    class Config:
        orm_mode = True


class CompanyCreate(BaseModel):
    name: str
    detail: str

    class Config:
        orm_mode = True


class CompanyUpdate(BaseModel):
    rid: int
    name: str
    detail: str

    class Config:
        orm_mode = True
