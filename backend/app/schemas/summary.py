from app.schemas import base as schema_base
from app.schemas import company as schema_company


class SummaryAmount(schema_base.ORMBaseModel):
    rid: int
    date_snap: str
    rank: int
    quarter1_expected: int
    quarter1_order: int
    quarter2_expected: int
    quarter2_order: int
    quarter3_expected: int
    quarter3_order: int
    quarter4_expected: int
    quarter4_order: int
    half_first_expected: int
    half_first_order: int
    half_second_expected: int
    half_second_order: int
    all_expected: int
    all_order: int


class SummaryCompany(schema_base.ORMBaseModel):
    rid: int
    date_snap: str
    company: schema_company.Company
    rank: int
    quarter1_expected: int
    quarter1_order: int
    quarter2_expected: int
    quarter2_order: int
    quarter3_expected: int
    quarter3_order: int
    quarter4_expected: int
    quarter4_order: int
    half_first_expected: int
    half_first_order: int
    half_second_expected: int
    half_second_order: int
    all_expected: int
    all_order: int


class SummaryCreate(schema_base.ORMBaseModel):
    date_snap: str
