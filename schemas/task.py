from pydantic import BaseModel, Field


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
