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
async def read_user_tasks(db: Session = Depends(get_db), username: str = Depends(JWTBearer()), skip: int = 0, limit: int = 100):
    db_tasks = get_all_user_tasks(db=db, username=username, skip=skip, limit=limit)
    return db_tasks


#2 Create a new task [A handler for creating a task]
@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(JWTBearer())])
async def post_task(task: TaskCreate, db: Session = Depends(get_db), username: str = Depends(JWTBearer())):
    db_task = get_task_by_title(db=db, task_title=task.title, username=username)
    if db_task:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Task with this title already exists."
        )
    create_task(db=db, task=task, username=username)
    return db_task


#3 Read Task by id [Get task by task id]
@router.get("/{task_id}", response_model=Task, dependencies=[Depends(JWTBearer())])
async def read_task_by_id(task_id: int, db: Session = Depends(get_db), username: str = Depends(JWTBearer())):
    db_task = get_task_by_id(db=db, task_id=task_id, username=username)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task with this task id does not exist."
        )
    return db_task


#4 Update a task [Update a task]
@router.post("/{task_id}", response_model=Task, dependencies=[Depends(JWTBearer())])
async def update_task_by_id(task_id: int, updated_task: TaskUpdate, db: Session = Depends(get_db), username: str = Depends(JWTBearer())):
    db_task = get_task_by_id(db=db, task_id=task_id, username=username)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task with this task id does not exist."
        )
    update_task(db=db, task_id=task_id, task=updated_task, username=username)
    return db_task


# 5 Delete a task [Delete a task]
@router.delete("/{task_id}", response_model=Task, dependencies=[Depends(JWTBearer())])
async def delete_task_by_id(task_id: int, db: Session = Depends(get_db), username: str = Depends(JWTBearer())):
    db_task = get_task_by_id(db=db, task_id=task_id, username=username)
    if db_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task with this task id does not exist."
        )
    delete_task(db=db, task_id=task_id, username=username)
    return db_task
