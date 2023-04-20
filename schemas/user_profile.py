from datetime import datetime
from pydantic import BaseModel
from typing import Optional

from .task import Task


class UserProfileBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserProfileCreate(UserProfileBase):
    username: str


class UserProfileUpdate(UserProfileBase):
    pass


class UserProfile(UserProfileBase):
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    tasks: list[Task] = []

    class Config:
        orm_mode = True