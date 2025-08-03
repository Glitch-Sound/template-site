from enum import IntEnum

from app.database import Base
from app.models.mixin import TimestampMixin
from sqlalchemy import Boolean, Column, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship


# fmt: off
class TypeNumber(IntEnum):
    NONE = 0
    M    = 1
    S    = 1
    O    = 2  # noqa: E741


class ProjectNumber(Base, TimestampMixin):
    __tablename__ = "project_numbers"

    rid          = Column(Integer, primary_key=True)
    rid_projects = Column(Integer, ForeignKey("projects.rid"))
    type         = Column(Integer, default=TypeNumber.NONE.value)
    number       = Column(String,  default="")
    date_start   = Column(String,  default="")
    date_end     = Column(String,  default="")
    is_deleted   = Column(Boolean, default=False)

    project = relationship("Project", back_populates="project_numbers", foreign_keys=[rid_projects])

    __table_args__ = (
        Index("idx_project_numbers_01", "is_deleted", "type", "rid"),
    )
# fmt: on
