from app.database import Base
from app.models.mixin import TimestampMixin
from sqlalchemy import Boolean, Column, Index, Integer, String
from sqlalchemy.orm import relationship


# fmt: off
class Company(Base, TimestampMixin):
    __tablename__ = "companies"

    rid        = Column(Integer, primary_key=True)
    name       = Column(String,  nullable=False, default="")
    detail     = Column(String,  nullable=False, default="")
    is_deleted = Column(Boolean, nullable=False, default=0)

    project_groups = relationship("ProjectGroup", back_populates="company", foreign_keys="ProjectGroup.rid_companies")

    __table_args__ = (
        Index("idx_companies_01", "is_deleted", "rid"),
    )
# fmt: on
