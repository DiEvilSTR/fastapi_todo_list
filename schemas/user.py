from datetime import datetime
from pydantic import BaseModel

from .task import Task


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    username: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    tasks: list[Task] = []

    class Config:
        orm_mode = True
