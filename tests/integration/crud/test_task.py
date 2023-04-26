from sqlalchemy.orm import Session

from crud import crud_task
from schemas.task import TaskCreate, TaskUpdate
from tests.utils.user import create_random_user
from tests.utils.utils import random_lower_string


def test_create_task(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    new_task = TaskCreate(title=title, description=description, is_done=True)
    user = create_random_user(db)
    task = crud_task.create_task(db=db, task=new_task, username=user.username)
    assert task.title == title
    assert task.description == description
    assert task.is_done == True
    assert task.created_by == user.username


def test_get_task_by_id(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    new_task = TaskCreate(title=title, description=description)
    user = create_random_user(db)
    task = crud_task.create_task(db=db, task=new_task, username=user.username)
    db_task = crud_task.get_task_by_id(db=db, task_id=task.id)
    assert db_task
    assert task.id == db_task.id
    assert task.title == db_task.title
    assert task.description == db_task.description
    assert task.is_done == db_task.is_done
    assert task.created_by == db_task.created_by


def test_get_task_by_title(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    new_task = TaskCreate(title=title, description=description)
    user = create_random_user(db)
    task = crud_task.create_task(db=db, task=new_task, username=user.username)
    db_task = crud_task.get_task_by_title(db=db, task_title=title, username=user.username)
    assert db_task
    assert task.id == db_task.id
    assert task.title == db_task.title
    assert task.description == db_task.description
    assert task.is_done == db_task.is_done
    assert task.created_by == db_task.created_by


def test_get_all_user_tasks(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    new_task = TaskCreate(title=title, description=description)
    user = create_random_user(db)
    task = crud_task.create_task(db=db, task=new_task, username=user.username)
    db_tasks = crud_task.get_all_user_tasks(db=db, username=user.username)
    assert db_tasks
    assert len(db_tasks) == 1
    assert task.id == db_tasks[0].id
    assert task.title == db_tasks[0].title
    assert task.description == db_tasks[0].description
    assert task.is_done == db_tasks[0].is_done
    assert task.created_by == db_tasks[0].created_by


def test_update_task(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    new_task = TaskCreate(title=title, description=description)
    user = create_random_user(db)
    task = crud_task.create_task(db=db, task=new_task, username=user.username)
    new_title = random_lower_string()
    new_description = random_lower_string()
    new_is_done = False
    updated_task = TaskUpdate(title=new_title, description=new_description, is_done=new_is_done)
    db_task = crud_task.update_task(db=db, task_id=task.id, task=updated_task)
    assert db_task
    assert db_task.id == task.id
    assert db_task.title == new_title
    assert db_task.description == new_description
    assert db_task.is_done == new_is_done
    assert db_task.created_by == user.username


def test_delete_task(db: Session) -> None:
    title = random_lower_string()
    description = random_lower_string()
    new_task = TaskCreate(title=title, description=description)
    user = create_random_user(db)
    task = crud_task.create_task(db=db, task=new_task, username=user.username)
    db_task = crud_task.delete_task(db=db, task_id=task.id)
    assert db_task
    assert db_task.id == task.id
    assert db_task.title == task.title
    assert db_task.description == task.description
    assert db_task.is_done == task.is_done
    assert db_task.created_by == task.created_by
    db_task = crud_task.get_task_by_id(db=db, task_id=task.id)
    assert db_task is None