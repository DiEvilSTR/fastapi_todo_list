from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from db.db_setup import Base
from .mixins import Timestamp


class User(Timestamp, Base):
    __tablename__ = "users"

    username = Column(String(16), nullable=False, primary_key=True, unique=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)

    profile = relationship("UserProfile", back_populates="owner", uselist=False, cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="task_owner", cascade="all, delete-orphan")


class UserProfile(Timestamp, Base):
    __tablename__ = "user_profiles"

    username = Column(String(16), ForeignKey("users.username"), primary_key=True, nullable=False)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)

    owner = relationship("User", back_populates="profile")