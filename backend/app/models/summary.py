from enum import IntEnum

from app.database import Base
from app.models import project as model_project
from app.models.mixin import TimestampMixin
from sqlalchemy import Column, Index, Integer, String


# fmt: off
class TypeSummary(IntEnum):
    NONE    = 0
    COMPANY = 1
    PROJECT = 2
    USER_PM = 3
    USER_PL = 4


class SummaryTotal(Base, TimestampMixin):
    __tablename__ = "summaries_total"

    rid        = Column(Integer, primary_key=True)
    date_snap  = Column(String,  nullable=False, default="")
    type       = Column(Integer, nullable=False, default=TypeSummary.NONE.value)
    rid_dim    = Column(Integer, nullable=False, default=0)
    expected   = Column(Integer, nullable=False, default=0)
    order      = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        Index("idx_summaries_total_01", "date_snap", "type", "rid_dim"),
    )


class SummaryCount(Base, TimestampMixin):
    __tablename__ = "summaries_count"

    rid        = Column(Integer, primary_key=True)
    date_snap  = Column(String,  nullable=False, default="")
    type       = Column(Integer, nullable=False, default=TypeSummary.NONE.value)
    rid_dim    = Column(Integer, nullable=False, default=0)
    rank       = Column(Integer, nullable=False, default=model_project.TypeRank.NONE.value)
    count      = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        Index("idx_summaries_count_01", "date_snap", "type", "rid_dim", "rank"),
    )
# fmt: on
