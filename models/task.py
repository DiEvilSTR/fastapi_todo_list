from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.db_setup import Base
from .mixins import Timestamp


class Task(Timestamp, Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), nullable=False)
    description = Column(String(200), nullable=True)
    is_done = Column(Boolean, default=False)
    created_by = Column(String, ForeignKey("users.username"), nullable=False)

    task_owner = relationship("User", back_populates="tasks", uselist=False)