from enum import IntEnum

from app.database import Base
from app.models.mixin import TimestampMixin
from sqlalchemy import Boolean, Column, Index, Integer, String
from sqlalchemy.orm import relationship


# fmt: off
class TypePost(IntEnum):
    NONE    = 0
    K       = 1
    C       = 2
    L       = 3
    T       = 4
    BP      = 5


class TypeContract(IntEnum):
    NONE      = 0
    PROPER    = 1
    TEMP      = 2
    CONSIGN_C = 3
    CONSIGN_M = 4


class User(Base, TimestampMixin):
    __tablename__ = "users"

    rid        = Column(Integer, primary_key=True)
    eid        = Column(String,  unique=True)
    username   = Column(String,  unique=True)
    password   = Column(String,  nullable=False, default="")
    name       = Column(String,  nullable=False, default="")
    company    = Column(String,  nullable=False, default="")
    post       = Column(Integer, nullable=False, default=TypePost.NONE.value)
    contract   = Column(Integer, nullable=False, default=TypeContract.NONE.value)
    price      = Column(Integer, nullable=False, default=0)
    is_admin   = Column(Boolean, nullable=False, default=0)
    is_deleted = Column(Boolean, nullable=False, default=0)

    projects_pm = relationship("Project", back_populates="user_pm", foreign_keys="Project.rid_users_pm")
    projects_pl = relationship("Project", back_populates="user_pl", foreign_keys="Project.rid_users_pl")

    threads     = relationship("Thread",  back_populates="user")

    __table_args__ = (
        Index("idx_users_01", "is_deleted", "rid"),
    )
# fmt: on
