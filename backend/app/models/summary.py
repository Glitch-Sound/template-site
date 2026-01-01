from app.database import Base
from app.models import project as model_project
from app.models.mixin import TimestampMixin
from sqlalchemy import Column, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship


# fmt: off
class SummaryAmount(Base, TimestampMixin):
    __tablename__ = "summaries_amount"

    rid                  = Column(Integer, primary_key=True)
    date_snap            = Column(String,  nullable=False, default="")
    rank                 = Column(Integer, nullable=False, default=model_project.TypeRank.NONE.value)
    quarter1_expected    = Column(Integer, nullable=False, default=0)
    quarter1_order       = Column(Integer, nullable=False, default=0)
    quarter2_expected    = Column(Integer, nullable=False, default=0)
    quarter2_order       = Column(Integer, nullable=False, default=0)
    quarter3_expected    = Column(Integer, nullable=False, default=0)
    quarter3_order       = Column(Integer, nullable=False, default=0)
    quarter4_expected    = Column(Integer, nullable=False, default=0)
    quarter4_order       = Column(Integer, nullable=False, default=0)
    half_first_expected  = Column(Integer, nullable=False, default=0)
    half_first_order     = Column(Integer, nullable=False, default=0)
    half_second_expected = Column(Integer, nullable=False, default=0)
    half_second_order    = Column(Integer, nullable=False, default=0)
    all_expected         = Column(Integer, nullable=False, default=0)
    all_order            = Column(Integer, nullable=False, default=0)

    __table_args__ = (
        Index("idx_summaries_amount_01", "date_snap", "rank"),
    )


class SummaryCompany(Base, TimestampMixin):
    __tablename__ = "summaries_company"

    rid                  = Column(Integer, primary_key=True)
    date_snap            = Column(String,  nullable=False, default="")
    rid_companies        = Column(Integer, ForeignKey("companies.rid"))
    rank                 = Column(Integer, nullable=False, default=model_project.TypeRank.NONE.value)
    quarter1_expected    = Column(Integer, nullable=False, default=0)
    quarter1_order       = Column(Integer, nullable=False, default=0)
    quarter2_expected    = Column(Integer, nullable=False, default=0)
    quarter2_order       = Column(Integer, nullable=False, default=0)
    quarter3_expected    = Column(Integer, nullable=False, default=0)
    quarter3_order       = Column(Integer, nullable=False, default=0)
    quarter4_expected    = Column(Integer, nullable=False, default=0)
    quarter4_order       = Column(Integer, nullable=False, default=0)
    half_first_expected  = Column(Integer, nullable=False, default=0)
    half_first_order     = Column(Integer, nullable=False, default=0)
    half_second_expected = Column(Integer, nullable=False, default=0)
    half_second_order    = Column(Integer, nullable=False, default=0)
    all_expected         = Column(Integer, nullable=False, default=0)
    all_order            = Column(Integer, nullable=False, default=0)

    company = relationship("Company", back_populates="summaries_company", foreign_keys=[rid_companies])

    __table_args__ = (
        Index("idx_summaries_company_01", "date_snap", "rid_companies", "rank"),
    )
# fmt: on
