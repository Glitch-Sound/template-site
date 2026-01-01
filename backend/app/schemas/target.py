from app.schemas import base as schema_base


class Target(schema_base.ORMBaseModel):
    rid: int
    year: int
    quarter1: int
    quarter2: int
    quarter3: int
    quarter4: int
    half_first: int
    half_second: int
    all: int


class TargetCreate(schema_base.ORMBaseModel):
    year: int
    quarter1: int
    quarter2: int
    quarter3: int
    quarter4: int


class TargetUpdate(schema_base.ORMBaseModel):
    rid: int
    year: int
    quarter1: int
    quarter2: int
    quarter3: int
    quarter4: int
