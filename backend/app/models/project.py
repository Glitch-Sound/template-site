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


class TypeQuarter(IntEnum):
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
    rank               = Column(Integer, nullable=False, default=TypeRank.NONE.value)
    pre_approval       = Column(String,  nullable=False, default="")
    name               = Column(String,  nullable=False, default="")
    number_parent      = Column(String,  nullable=False, default="")
    number_m           = Column(Boolean, nullable=False, default=0)
    number_s           = Column(Boolean, nullable=False, default=0)
    number_o           = Column(Boolean, nullable=False, default=0)
    amount_expected    = Column(Integer, nullable=False, default=0)
    amount_order       = Column(Integer, nullable=False, default=0)
    date_start         = Column(String,  nullable=False, default="")
    date_delivery      = Column(String,  nullable=False, default="")
    date_end           = Column(String,  nullable=False, default="")
    target_quarter     = Column(Integer, nullable=False, default=0)
    karte_plan         = Column(Boolean, nullable=False, default=0)
    karte_report       = Column(Boolean, nullable=False, default=0)
    checklist          = Column(Boolean, nullable=False, default=0)
    is_deleted         = Column(Boolean, nullable=False, default=0)

    project_group = relationship("ProjectGroup", back_populates="projects",    foreign_keys=[rid_project_groups])
    user_pm       = relationship("User",         back_populates="projects_pm", foreign_keys=[rid_users_pm])
    user_pl       = relationship("User",         back_populates="projects_pl", foreign_keys=[rid_users_pl])

    project_numbers = relationship("ProjectNumber", back_populates="project", foreign_keys="[ProjectNumber.rid_projects]")
    threads         = relationship("Thread",        back_populates="project", foreign_keys="[Thread.rid_projects]")

    __table_args__ = (
        Index("idx_projects_01", "is_deleted", "rid"),
        Index("idx_projects_02", "is_deleted", "target_quarter", "rid_users_pm", "rid_users_pl"),
        Index("idx_projects_03", "is_deleted", "target_quarter"),
        Index("idx_projects_04", "is_deleted", "rid_users_pm"),
        Index("idx_projects_05", "is_deleted", "rid_users_pl"),
    )
# fmt: on
