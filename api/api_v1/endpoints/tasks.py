from fastapi import Depends, APIRouter, HTTPException, status
from typing import Optional

from core.jwt_authentication.jwt_bearer import JWTBearer
from schemas.task import TaskSchema

tasks = [
    {
        "id": 1,
        "title": "To eat",
        "description": "To eat something after porka"
    },
    {
        "id": 2,
        "title": "Porka again",
        "description": "To porka after something food"
    },
    {
        "id": 1,
        "title": "To eat again",
        "description": "To eat something again after porka"
    },
]

router = APIRouter()

@router.get("/{task_id}")
def get_task_by_id(task_id: Optional[int] = None):
    if task_id > len(tasks):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task with this ID does not exists."
        )
    for task in tasks:
        if task["id"] == task_id:
            return {"data": task}


#4 Post a new task [A handler for creating a task]
@router.post("/", dependencies=[Depends(JWTBearer())])
def post_task(task: TaskSchema):
    task.id = len(tasks) + 1
    tasks.append(task.dict())
    return {
        "data": "Task Added!"
    }