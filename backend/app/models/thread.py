from enum import IntEnum

from app.database import Base
from app.models.mixin import TimestampMixin
from sqlalchemy import Boolean, Column, ForeignKey, Index, Integer, String
from sqlalchemy.orm import relationship


# fmt: off
class TypeThreadState(IntEnum):
    NONE      = 0
    RUN       = 1
    IMPORTANT = 2
    COMPLETED = 3


class Thread(Base, TimestampMixin):
    __tablename__ = "threads"

    rid          = Column(Integer, primary_key=True)
    rid_projects = Column(Integer, ForeignKey("projects.rid"))
    rid_parent   = Column(Integer, ForeignKey("threads.rid"))
    rid_users    = Column(Integer, ForeignKey("users.rid"))
    state        = Column(Integer, nullable=False, default=TypeThreadState.NONE.value)
    note         = Column(String,  nullable=False, default="")
    is_deleted   = Column(Boolean, nullable=False, default=0)

    project = relationship("Project", back_populates="threads", foreign_keys=[rid_projects])
    user    = relationship("User",    back_populates="threads", foreign_keys=[rid_users])

    parent   = relationship("Thread", remote_side=[rid], back_populates="children", foreign_keys=[rid_parent])
    children = relationship("Thread", back_populates="parent", foreign_keys=[rid_parent], order_by="Thread.created_at", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_threads_01", "is_deleted", "rid"),
    )
# fmt: on
