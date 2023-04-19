from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(TaskBase):
    title: Optional[str] = None
    description: Optional[str] = None
    is_done: Optional[bool] = False


class Task(TaskBase):
    id: int
    title: str
    description: Optional[str] = None
    is_done: bool
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
