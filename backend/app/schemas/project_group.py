from pydantic import BaseModel


class ProjectGroup(BaseModel):
    rid: int
    rid_companies: int
    name: str
    detail: str

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
