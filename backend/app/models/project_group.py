from app.database import Base
from app.models.mixin import TimestampMixin
from sqlalchemy import Boolean, Column, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship


# fmt: off
class ProjectGroup(Base, TimestampMixin):
    __tablename__ = "project_groups"

    rid           = Column(Integer, primary_key=True)
    rid_companies = Column(Integer, ForeignKey("companies.rid"))
    name          = Column(String,  nullable=False, default="")
    detail        = Column(String,  nullable=False, default="")
    is_deleted    = Column(Boolean, nullable=False, default=0,)

    company = relationship("Company", back_populates="project_groups", foreign_keys=[rid_companies])

    projects = relationship("Project", back_populates="project_group", foreign_keys="[Project.rid_project_groups]")

    __table_args__ = (
        Index("idx_project_groups_01", "is_deleted", "rid"),
    )
# fmt: on
