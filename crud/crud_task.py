from sqlalchemy import and_
from sqlalchemy.orm import Session

from models.task import Task
from schemas.task import TaskCreate, TaskUpdate

def get_task_by_id(db: Session, task_id: int):
    return db.query(Task).filter(Task.id == task_id).first()


# For checking if the task exists or not
def get_task_by_title(db: Session, task_title: str, username: str):
    return db.query(Task).filter(and_(Task.title == task_title, Task.created_by == username)).first()


def get_all_user_tasks(db: Session, username: str, skip: int = 0, limit: int = 100):
    return db.query(Task).filter(Task.created_by == username).offset(skip).limit(limit).all()


def create_task(db: Session, task: TaskCreate, username: str):
    db_task = Task(**task.dict(), created_by=username)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(db: Session, task_id: int, task: TaskUpdate):
    db_task = get_task_by_id(db=db, task_id=task_id)
    updated_task = task.dict(exclude_unset=True)
    for key, value in updated_task.items():
            setattr(db_task, key, value)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int):
    db_task = get_task_by_id(db=db, task_id=task_id)
    db.delete(db_task)
    db.commit()
    return db_task