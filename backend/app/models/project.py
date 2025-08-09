from enum import IntEnum

from app.database import Base
from app.models.mixin import TimestampMixin
from sqlalchemy import Boolean, Column, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship


# fmt: off
class TypeRank(IntEnum):
    NONE = 0
    A    = 1
    B    = 2
    C    = 3
    D    = 4
    E    = 5


class Quarter(IntEnum):
    NONE = 0
    Q1   = 1
    Q2   = 2
    Q3   = 3
    Q4   = 4


class Project(Base, TimestampMixin):
    __tablename__ = "projects"

    rid                = Column(Integer, primary_key=True)
    rid_project_groups = Column(Integer, ForeignKey("project_groups.rid"))
    rid_users_pm       = Column(Integer, ForeignKey("users.rid"))
    rid_users_pl       = Column(Integer, ForeignKey("users.rid"))
    rank               = Column(Integer, default=TypeRank.NONE.value)
    pre_approval       = Column(String,  default="")
    name               = Column(String,  default="")
    number_parent      = Column(String,  default="")
    number_m           = Column(Boolean, default=False)
    number_s           = Column(Boolean, default=False)
    number_o           = Column(Boolean, default=False)
    amount_expected    = Column(Integer, default=0)
    amount_order       = Column(Integer, default=0)
    date_start         = Column(String,  default="")
    date_delivery      = Column(String,  default="")
    date_end           = Column(String,  default="")
    karte_plan         = Column(Boolean, default=False)
    karte_report       = Column(Boolean, default=False)
    checklist          = Column(Boolean, default=False)
    is_deleted         = Column(Boolean, default=False)

    project_group = relationship("ProjectGroup", back_populates="projects",    foreign_keys=[rid_project_groups])
    user_pm       = relationship("User",         back_populates="projects_pm", foreign_keys=[rid_users_pm])
    user_pl       = relationship("User",         back_populates="projects_pl", foreign_keys=[rid_users_pl])

    project_numbers = relationship("ProjectNumber", back_populates="project", foreign_keys="[ProjectNumber.rid_projects]")

    __table_args__ = (
        Index("idx_projects_01", "is_deleted", "rid"),
    )
# fmt: on
