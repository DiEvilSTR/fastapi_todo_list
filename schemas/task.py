from datetime import datetime
from pydantic import BaseModel, Field

# TODO: Use this TaskBase, TaskCreate, Task in endpoints
class TaskBase(BaseModel):
    title: str
    description: str | None = None


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    id: int
    title: str
    description: str | None = None
    is_done: bool
    created_by: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


# TODO: Stop using this and delete it
class TaskSchema(BaseModel):
    id: int = Field(default=None)
    title: str = Field(default=None)
    description: str = Field(default=None)

    class Config:
        schema_extra = {
            "task_demo": {
                "title": "Porka",
                "description": "Porka 24 hours"}
        }
