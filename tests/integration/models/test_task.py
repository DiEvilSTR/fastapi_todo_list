import pytest

from datetime import datetime

from models.task import Task
from models.user import User, UserProfile
from tests.conftest import get_test_db


def test_task_model(get_test_db):
    with get_test_db as db:
        # Create a new user and save it to the database
        username = "test_user"
        hashed_password = "test_password"
        user = User(username=username, hashed_password=hashed_password)
        db.add(user)
        db.commit()

        # Create a new user profile and save it to the database
        first_name="test_first_name"
        last_name="test_last_name"
        user_profile = UserProfile(username=username, first_name=first_name, last_name=last_name)
        db.add(user_profile)
        db.commit()

        # Create a new task and save it to the database
        task_name = "test_task"
        task_description = "test_description"
        task = Task(title=task_name, description=task_description, created_by=username)
        db.add(task)
        db.commit()

        # Retrieve the task from the database and check that its attributes match the input
        db_test_task = db.query(Task).filter_by(title=task_name).first()
        assert type(db_test_task.id)==int, \
            f"Expected id to be int, got {type(db_test_task.id)}"
        assert db_test_task.title == task_name, \
            f"Expected task_name to be {task_name}, got {db_test_task.title}"
        assert db_test_task.description == task_description, \
            f"Expected task_description to be {task_description}, got {db_test_task.description}"
        assert db_test_task.is_done == False, \
            f"Expected is_done to be False, got {db_test_task.is_done}"

        # Test that the Timestamp columns were automatically populated
        assert isinstance(db_test_task.created_at, datetime), \
            f"Expected created_at to be datetime, got {type(db_test_task.created_at)}"
        assert isinstance(db_test_task.updated_at, datetime), \
            f"Expected updated_at to be datetime, got {type(db_test_task.updated_at)}"
        assert db_test_task.created_at == db_test_task.updated_at, \
            "Expected created_at and updated_at to be equal"

        # Delete the user from the database
        db_test_user = db.query(User).filter_by(username=username).first()
        db.delete(db_test_user)
        db.commit()

        # Check that the task was automatically deleted
        db_test_task = db.query(Task).filter_by(title=task_name).first()
        assert db_test_task == None, \
            "Expected task to be None"