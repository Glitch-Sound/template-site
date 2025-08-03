from app.schemas import company as schema_company
from pydantic import BaseModel


class ProjectGroup(BaseModel):
    rid: int
    name: str
    detail: str
    company: schema_company.Company

    class Config:
        orm_mode = True


class ProjectGroupCreate(BaseModel):
    rid_companies: int
    name: str
    detail: str

    class Config:
        orm_mode = True


class ProjectGroupUpdate(BaseModel):
    rid: int
    rid_companies: int
    name: str
    detail: str

    class Config:
        orm_mode = True


class Project(BaseModel):
    rid: int
    rid_project_groups: int
    rid_users_pm: int
    rid_users_pl: int
    rank: int
    title: str
    amount_expected: int
    amount_order: int
    date_start: str
    date_delivery: str
    date_end: str
    karte_plan: int
    karte_report: int
    checklist: int
    no_parent: str

    class Config:
        orm_mode = True


class ProjectCreate(BaseModel):
    rid_companies: int
    rid_project_groups: int
    rid_users_pm: int
    rid_users_pl: int
    rank: int
    title: str
    amount_expected: int
    amount_order: int
    date_start: str
    date_delivery: str
    date_end: str
    karte_plan: int
    karte_report: int
    checklist: int
    no_parent: str

    class Config:
        orm_mode = True


class ProjectUpdate(BaseModel):
    rid: int
    rid_project_groups: int
    rid_users_pm: int
    rid_users_pl: int
    rank: int
    title: str
    amount_expected: int
    amount_order: int
    date_start: str
    date_delivery: str
    date_end: str
    karte_plan: int
    karte_report: int
    checklist: int
    no_parent: str

    class Config:
        orm_mode = True
