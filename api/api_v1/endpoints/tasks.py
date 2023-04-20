from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import List, Optional
from sqlalchemy.orm import Session

from core.jwt_authentication.jwt_bearer import JWTBearer
from schemas.task import Task, TaskCreate, TaskUpdate

from crud.crud_task import create_task, delete_task, get_all_user_tasks, get_task_by_id, get_task_by_title, update_task
from db.db_setup import get_db


router = APIRouter()


#1 Read all Tasks [Get list of user's tasks]
@router.get("/", response_model=List[Task], dependencies=[Depends(JWTBearer())])
def read_user_tasks(db: Session = Depends(get_db), current_user: str = Depends(JWTBearer()), skip: int = 0, limit: int = 100):
    db_tasks = get_all_user_tasks(db=db, username=current_user, skip=skip, limit=limit)
    return db_tasks


#2 Create a new task [A handler for creating a task]
@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())])
def post_task(task: TaskCreate, db: Session = Depends(get_db), current_user: str = Depends(JWTBearer())):
    db_task = get_task_by_title(db=db, task_title=task.title, username=current_user)
    if db_task:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Task with this title already exists."
        )
    db_task = create_task(db=db, task=task, username=current_user)
    return db_task


#3 Read Task by id [Get task by task id]
@router.get("/{task_id}", response_model=Task, dependencies=[Depends(JWTBearer())])
def read_task_by_id(task_id: int, db: Session = Depends(get_db)):
    db_task = get_task_by_id(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task with this task id does not exist."
        )
    return db_task


#4 Update a task [Update a task]
@router.patch("/{task_id}", response_model=Task, dependencies=[Depends(JWTBearer())])
def update_task_by_id(task_id: int, updated_task: TaskUpdate, db: Session = Depends(get_db), current_user: str = Depends(JWTBearer())):
    db_task = get_task_by_id(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task with this task id does not exist."
        )
    if db_task.created_by != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to update this task."
        )
    update_task(db=db, task_id=task_id, task=updated_task)
    return db_task


# 5 Delete a task [Delete a task]
@router.delete("/{task_id}", response_model=Task, dependencies=[Depends(JWTBearer())])
def delete_task_by_id(task_id: int, db: Session = Depends(get_db), current_user: str = Depends(JWTBearer())):
    db_task = get_task_by_id(db=db, task_id=task_id)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task with this task id does not exist."
        )
    if db_task.created_by != current_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this task."
        )
    delete_task(db=db, task_id=task_id)
    return db_task
