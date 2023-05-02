from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from core.jwt_authentication.jwt_bearer import jwt_scheme
from crud import crud_task
from db.db_setup import get_db
from schemas.task import Task, TaskCreate, TaskUpdate

router = APIRouter()


#1 Read all Tasks [Get list of user's tasks]
@router.get("/", response_model=List[Task], dependencies=[Depends(jwt_scheme)])
def read_user_tasks(db: Session = Depends(get_db), current_user: str = Depends(jwt_scheme), skip: int = 0, limit: int = 100):
    db_tasks = crud_task.get_all_user_tasks(db=db, username=current_user, skip=skip, limit=limit)
    return db_tasks


#2 Create a new task [A handler for creating a task]
@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(jwt_scheme)])
def post_task(task: TaskCreate, db: Session = Depends(get_db), current_user: str = Depends(jwt_scheme)):
    db_task = crud_task.get_task_by_title(db=db, task_title=task.title, username=current_user)
    if db_task:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Task with this title already exists."
        )
    db_task = crud_task.create_task(db=db, task=task, username=current_user)
    return db_task


#3 Read Task by id [Get task by task id]
@router.get("/{task_id}", response_model=Task, dependencies=[Depends(jwt_scheme)])
def read_task_by_id(task_id: int, db: Session = Depends(get_db)):
    db_task = crud_task.get_task_by_id(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task with this task id does not exist."
        )
    return db_task


#4 Update a task [Update a task]
@router.patch("/{task_id}", response_model=Task, dependencies=[Depends(jwt_scheme)])
def update_task_by_id(task_id: int, updated_task: TaskUpdate, db: Session = Depends(get_db), current_user: str = Depends(jwt_scheme)):
    db_task = crud_task.get_task_by_id(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task with this task id does not exist."
        )
    if db_task.created_by != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update this task."
        )
    crud_task.update_task(db=db, task_id=task_id, task=updated_task)
    return db_task


# 5 Delete a task [Delete a task]
@router.delete("/{task_id}", response_model=Task, dependencies=[Depends(jwt_scheme)])
def delete_task_by_id(task_id: int, db: Session = Depends(get_db), current_user: str = Depends(jwt_scheme)):
    db_task = crud_task.get_task_by_id(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task with this task id does not exist."
        )
    if db_task.created_by != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this task."
        )
    crud_task.delete_task(db=db, task_id=task_id)
    return db_task
