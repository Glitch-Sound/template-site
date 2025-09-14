from app.schemas import base as schema_base


class Company(schema_base.ORMBaseModel):
    rid: int
    name: str
    detail: str


class CompanyCreate(schema_base.ORMBaseModel):
    name: str
    detail: str


class CompanyUpdate(schema_base.ORMBaseModel):
    rid: int
    name: str
    detail: str
