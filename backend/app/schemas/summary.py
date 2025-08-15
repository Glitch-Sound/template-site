from app.schemas import company as schema_company
from app.schemas import project as schema_project
from app.schemas import user as schema_user
from pydantic import BaseModel


class SummaryTotalCompany(BaseModel):
    rid: int
    date_snap: str
    company: schema_company.Company
    expected: int
    order: int

    class Config:
        orm_mode = True


class SummaryTotalProject(BaseModel):
    rid: int
    date_snap: str
    project: schema_project.ProjectGroup
    expected: int
    order: int

    class Config:
        orm_mode = True


class SummaryTotalPM(BaseModel):
    rid: int
    date_snap: str
    user_pm: schema_user.User
    expected: int
    order: int

    class Config:
        orm_mode = True


class SummaryTotalPL(BaseModel):
    rid: int
    date_snap: str
    user_pl: schema_user.User
    expected: int
    order: int

    class Config:
        orm_mode = True


class SummaryCountCompany(BaseModel):
    rid: int
    date_snap: str
    company: schema_company.Company
    count: int

    class Config:
        orm_mode = True


class SummaryCountProject(BaseModel):
    rid: int
    date_snap: str
    project: schema_project.ProjectGroup
    count: int

    class Config:
        orm_mode = True


class SummaryCountPM(BaseModel):
    rid: int
    date_snap: str
    user_pm: schema_user.User
    count: int

    class Config:
        orm_mode = True


class SummaryCountPL(BaseModel):
    rid: int
    date_snap: str
    user_pl: schema_user.User
    count: int

    class Config:
        orm_mode = True


class SummaryCreate(BaseModel):
    date_snap: str

    class Config:
        orm_mode = True
