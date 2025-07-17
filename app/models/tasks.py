### Tableの定義 ###
import os
import sys
import uuid

from sqlalchemy import TEXT, Column, DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import backref, relationship

sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), ".."))
from app.db.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(
        String(length=36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    title = Column(String(length=255))
    description = Column(TEXT)
    status = Column(SqlEnum("TODO", "In progress", "Done"))
    priority = Column(SqlEnum("Low", "Medium", "High"))
    deadline = Column(DateTime)
    created_at = Column(DateTime)
    created_by = Column(String(length=36))
    updated_at = Column(DateTime)

    class Config:
        orm_mode = True


class User(Base):
    __tablename__ = "users"

    id = Column(
        String(length=36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
        unique=True,
        nullable=False,
    )
    email = Column(String(length=255))
    password = Column(String(length=255))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)

    class Config:
        orm_mode = True
