from app.database import Base
from sqlalchemy import Column, Integer, String


class User(Base):
    __tablename__ = "users"

    # fmt: off
    rid      = Column(Integer, primary_key=True)
    user     = Column(String,  unique=True)
    password = Column(String,  default="")
    name     = Column(String,  default="")
    # fmt: on
