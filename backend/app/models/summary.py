from app.database import Base
from app.models import project as model_project
from app.models.mixin import TimestampMixin
from sqlalchemy import Column, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship


# fmt: off
class SummaryTotalCompany(Base, TimestampMixin):
    __tablename__ = "summaries_total_company"

    rid            = Column(Integer, primary_key=True)
    date_snap      = Column(String,  nullable=False, default="")
    rid_companies  = Column(Integer, ForeignKey("companies.rid"))
    total_expected = Column(Integer, nullable=False, default=0)
    total_order    = Column(Integer, nullable=False, default=0)

    company = relationship("Company", back_populates="summaries_total_company", foreign_keys=[rid_companies])

    __table_args__ = (
        Index("idx_summaries_total_company_01", "date_snap", "rid_companies"),
    )


class SummaryTotalProject(Base, TimestampMixin):
    __tablename__ = "summaries_total_project"

    rid                = Column(Integer, primary_key=True)
    date_snap          = Column(String,  nullable=False, default="")
    rid_project_groups = Column(Integer, ForeignKey("project_groups.rid"))
    total_expected     = Column(Integer, nullable=False, default=0)
    total_order        = Column(Integer, nullable=False, default=0)

    project_group = relationship("ProjectGroup", back_populates="summaries_total_project", foreign_keys=[rid_project_groups])

    __table_args__ = (
        Index("idx_summaries_total_project_01", "date_snap", "rid_project_groups"),
    )


class SummaryTotalPM(Base, TimestampMixin):
    __tablename__ = "summaries_total_pm"

    rid            = Column(Integer, primary_key=True)
    date_snap      = Column(String,  nullable=False, default="")
    rid_users_pm   = Column(Integer, ForeignKey("users.rid"))
    total_expected = Column(Integer, nullable=False, default=0)
    total_order    = Column(Integer, nullable=False, default=0)

    user_pm = relationship("User", back_populates="summaries_total_pm", foreign_keys=[rid_users_pm])

    __table_args__ = (
        Index("idx_summaries_total_pm_01", "date_snap", "rid_users_pm"),
    )



class SummaryTotalPL(Base, TimestampMixin):
    __tablename__ = "summaries_total_pl"

    rid            = Column(Integer, primary_key=True)
    date_snap      = Column(String,  nullable=False, default="")
    rid_users_pl   = Column(Integer, ForeignKey("users.rid"))
    total_expected = Column(Integer, nullable=False, default=0)
    total_order    = Column(Integer, nullable=False, default=0)

    user_pl = relationship("User", back_populates="summaries_total_pl", foreign_keys=[rid_users_pl])

    __table_args__ = (
        Index("idx_summaries_total_pl_01", "date_snap", "rid_users_pl"),
    )



class SummaryCountCompany(Base, TimestampMixin):
    __tablename__ = "summaries_count_company"

    rid           = Column(Integer, primary_key=True)
    date_snap     = Column(String,  nullable=False, default="")
    rid_companies = Column(Integer, ForeignKey("companies.rid"))
    rank          = Column(Integer, nullable=False, default=model_project.TypeRank.NONE.value)
    count         = Column(Integer, nullable=False, default=0)

    company = relationship("Company", back_populates="summaries_count_company", foreign_keys=[rid_companies])

    __table_args__ = (
        Index("idx_summaries_count_company_01", "date_snap", "rid_companies", "rank"),
    )


class SummaryCountProject(Base, TimestampMixin):
    __tablename__ = "summaries_count_project"

    rid                = Column(Integer, primary_key=True)
    date_snap          = Column(String,  nullable=False, default="")
    rid_project_groups = Column(Integer, ForeignKey("project_groups.rid"))
    rank               = Column(Integer, nullable=False, default=model_project.TypeRank.NONE.value)
    count              = Column(Integer, nullable=False, default=0)

    project_group = relationship("ProjectGroup", back_populates="summaries_count_project", foreign_keys=[rid_project_groups])

    __table_args__ = (
        Index("idx_summaries_count_project_01", "date_snap", "rid_project_groups", "rank"),
    )


class SummaryCountPM(Base, TimestampMixin):
    __tablename__ = "summaries_count_pm"

    rid          = Column(Integer, primary_key=True)
    date_snap    = Column(String,  nullable=False, default="")
    rid_users_pm = Column(Integer, ForeignKey("users.rid"))
    rank         = Column(Integer, nullable=False, default=model_project.TypeRank.NONE.value)
    count        = Column(Integer, nullable=False, default=0)

    user_pm = relationship("User", back_populates="summaries_count_pm", foreign_keys=[rid_users_pm])

    __table_args__ = (
        Index("idx_summaries_count_pm_01", "date_snap", "rid_users_pm", "rank"),
    )


class SummaryCountPL(Base, TimestampMixin):
    __tablename__ = "summaries_count_pl"

    rid          = Column(Integer, primary_key=True)
    date_snap    = Column(String,  nullable=False, default="")
    rid_users_pl = Column(Integer, ForeignKey("users.rid"))
    rank         = Column(Integer, nullable=False, default=model_project.TypeRank.NONE.value)
    count        = Column(Integer, nullable=False, default=0)

    user_pl = relationship("User", back_populates="summaries_count_pl", foreign_keys=[rid_users_pl])

    __table_args__ = (
        Index("idx_summaries_count_pl_01", "date_snap", "rid_users_pl", "rank"),
    )
# fmt: on
