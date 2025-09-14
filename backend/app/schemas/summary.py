from app.schemas import base as schema_base
from app.schemas import company as schema_company
from app.schemas import project as schema_project
from app.schemas import user as schema_user


class SummaryTotalCompany(schema_base.ORMBaseModel):
    rid: int
    date_snap: str
    company: schema_company.Company
    total_expected: int
    total_order: int


class SummaryTotalProject(schema_base.ORMBaseModel):
    rid: int
    date_snap: str
    project_group: schema_project.ProjectGroup
    total_expected: int
    total_order: int


class SummaryTotalPM(schema_base.ORMBaseModel):
    rid: int
    date_snap: str
    user_pm: schema_user.User
    total_expected: int
    total_order: int


class SummaryTotalPL(schema_base.ORMBaseModel):
    rid: int
    date_snap: str
    user_pl: schema_user.User
    total_expected: int
    total_order: int


class SummaryCountCompany(schema_base.ORMBaseModel):
    rid: int
    date_snap: str
    company: schema_company.Company
    rank: int
    count: int


class SummaryCountProject(schema_base.ORMBaseModel):
    rid: int
    date_snap: str
    project_group: schema_project.ProjectGroup
    rank: int
    count: int


class SummaryCountPM(schema_base.ORMBaseModel):
    rid: int
    date_snap: str
    user_pm: schema_user.User
    rank: int
    count: int


class SummaryCountPL(schema_base.ORMBaseModel):
    rid: int
    date_snap: str
    user_pl: schema_user.User
    rank: int
    count: int


class SummaryCreate(schema_base.ORMBaseModel):
    date_snap: str
