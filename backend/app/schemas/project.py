from typing import List, Optional

from app.models import project as model_project
from app.models import project_number as model_project_number
from app.schemas import company as schema_company
from app.schemas import user as schema_user
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


class ProjectNumber(BaseModel):
    rid: int
    type: model_project_number.TypeNumber
    number: str
    date_start: str
    date_end: str

    class Config:
        orm_mode = True


class ProjectNumberCreate(BaseModel):
    rid_projects: int
    type: model_project_number.TypeNumber
    number: str
    date_start: str
    date_end: str

    class Config:
        orm_mode = True


class ProjectNumberUpdate(BaseModel):
    rid: int
    rid_projects: int
    type: model_project_number.TypeNumber
    number: str
    date_start: str
    date_end: str

    class Config:
        orm_mode = True


class TargetQuarter(BaseModel):
    year: int
    quarter: model_project.TypeQuarter


class SearchCondition(BaseModel):
    target: List[TargetQuarter]
    rid_users_pm: List[int]
    rid_users_pl: List[int]
    is_none_pre_approval: bool
    is_none_number_m: bool
    is_none_number_s: bool
    is_none_number_o: bool


class Project(BaseModel):
    rid: int
    project_group: ProjectGroup
    user_pm: schema_user.User
    user_pl: schema_user.User
    rank: model_project.TypeRank
    pre_approval: str
    name: str
    number_parent: str
    numbers: Optional[List[ProjectNumber]] = []
    number_m: bool
    number_s: bool
    number_o: bool
    amount_expected: int
    amount_order: int
    date_start: str
    date_delivery: str
    date_end: str
    target_quarter: int
    karte_plan: bool
    karte_report: bool
    checklist: bool

    class Config:
        orm_mode = True


class ProjectCreate(BaseModel):
    rid_project_groups: int
    rid_users_pm: int
    rid_users_pl: int
    rank: int
    pre_approval: str
    name: str
    number_parent: str
    amount_expected: int
    amount_order: int
    date_start: str
    date_delivery: str
    date_end: str

    class Config:
        orm_mode = True


class ProjectUpdate(BaseModel):
    rid: int
    rid_project_groups: int
    rid_users_pm: int
    rid_users_pl: int
    rank: int
    pre_approval: str
    name: str
    number_parent: str
    amount_expected: int
    amount_order: int
    date_start: str
    date_delivery: str
    date_end: str

    class Config:
        orm_mode = True


class ProjectList(BaseModel):
    rid: int
    name: str
    company: schema_company.Company
    projects: List[Project]

    class Config:
        orm_mode = True
