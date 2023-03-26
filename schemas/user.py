from datetime import datetime
from pydantic import BaseModel, Field, EmailStr

from .task import Task


# TODO: Use this UserBase, UserCreate, User in endpoints
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


# TODO: Stop using this and delete it
# class UserSchema(BaseModel):
#     name: str = Field(default=None)
#     email: EmailStr = Field(default=None)
#     password: str = Field(default=None)

#     class Config:
#         the_schema = {
#             "user_demo": {
#                 "name": "Envy",
#                 "email": "envy@shmenvy.com",
#                 "password": "666"
#             }
#         }


class UserLoginSchema(BaseModel):
    email: EmailStr = Field(default=None)
    password: str = Field(default=None)

    class Config:
        the_schema = {
            "user_demo": {
                "email": "envy@shmenvy.com",
                "password": "666"
            }
        }
