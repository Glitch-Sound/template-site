from app.database import Base
from app.models.mixin import TimestampMixin
from sqlalchemy import Boolean, Column, Index, Integer


# fmt: off
class Target(Base, TimestampMixin):
    __tablename__ = "targets"

    rid         = Column(Integer, primary_key=True)
    year        = Column(Integer, nullable=False, default=0)
    quarter1    = Column(Integer, nullable=False, default=0)
    quarter2    = Column(Integer, nullable=False, default=0)
    quarter3    = Column(Integer, nullable=False, default=0)
    quarter4    = Column(Integer, nullable=False, default=0)
    half_first  = Column(Integer, nullable=False, default=0)
    half_second = Column(Integer, nullable=False, default=0)
    all         = Column(Integer, nullable=False, default=0)
    is_deleted  = Column(Boolean, nullable=False, default=0)

    __table_args__ = (
        Index("idx_targets_01", "is_deleted", "rid", "year"),
    )
# fmt: on
