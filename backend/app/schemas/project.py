from typing import List, Optional

from app.models import project as model_project
from app.models import project_number as model_project_number
from app.schemas import base as schema_base
from app.schemas import company as schema_company
from app.schemas import user as schema_user


class ProjectGroup(schema_base.ORMBaseModel):
    rid: int
    name: str
    detail: str
    company: schema_company.Company


class ProjectGroupCreate(schema_base.ORMBaseModel):
    rid_companies: int
    name: str
    detail: str


class ProjectGroupUpdate(schema_base.ORMBaseModel):
    rid: int
    rid_companies: int
    name: str
    detail: str


class ProjectNumber(schema_base.ORMBaseModel):
    rid: int
    type: model_project_number.TypeNumber
    number: str
    note: str
    date_start: str
    date_end: str


class ProjectNumberCreate(schema_base.ORMBaseModel):
    rid_projects: int
    type: model_project_number.TypeNumber
    number: str
    note: str
    date_start: str
    date_end: str


class ProjectNumberUpdate(schema_base.ORMBaseModel):
    rid: int
    rid_projects: int
    type: model_project_number.TypeNumber
    number: str
    note: str
    date_start: str
    date_end: str


class TargetQuarter(schema_base.ORMBaseModel):
    year: int
    quarter: model_project.TypeQuarter


class SearchCondition(schema_base.ORMBaseModel):
    target: List[int]
    rid_users_pm: List[int]
    rid_users_pl: List[int]
    is_none_pre_approval: bool
    is_none_number_m: bool
    is_none_number_s: bool
    is_none_number_o: bool


class Project(schema_base.ORMBaseModel):
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


class ProjectCreate(schema_base.ORMBaseModel):
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


class ProjectUpdate(schema_base.ORMBaseModel):
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


class ProjectList(schema_base.ORMBaseModel):
    rid: int
    name: str
    company: schema_company.Company
    projects: List[Project]
