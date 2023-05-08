import pytest

from datetime import datetime

from models.user import User, UserProfile
from tests.conftest import get_test_db


def test_user_model(get_test_db):
    with get_test_db as db:
        # Create a new user and save it to the database
        username = "test_user"
        hashed_password = "test_password"
        user = User(username=username, hashed_password=hashed_password)
        db.add(user)
        db.commit()

        # Retrieve the user from the database and check that its attributes match the input
        db_test_user = db.query(User).filter_by(username=username).first()
        assert db_test_user.username == username, \
            f"Expected username to be {username}, got {db_test_user.username}"
        assert db_test_user.hashed_password == hashed_password, \
            f"Expected hashed_password to be {hashed_password}, got {db_test_user.hashed_password}"

        # Test that the Timestamp columns were automatically populated
        assert isinstance(db_test_user.created_at, datetime), \
            f"Expected created_at to be datetime, got {type(db_test_user.created_at)}"
        assert isinstance(db_test_user.updated_at, datetime), \
            f"Expected updated_at to be datetime, got {type(db_test_user.updated_at)}"
        assert db_test_user.created_at == db_test_user.updated_at, \
            "Expected created_at and updated_at to be equal"

        # Delete the user from the database
        db.delete(db_test_user)
        db.commit()


def test_user_profile_model(get_test_db):
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

        # Retrieve the user from the database and check that its attributes match the input
        db_test_user_profile = db.query(UserProfile).filter_by(username=username).first()
        assert db_test_user_profile.username == username, \
            f"Expected username to be {username}, got {db_test_user_profile.username}"
        assert db_test_user_profile.first_name == first_name, \
            f"Expected first_name to be {first_name}, got {db_test_user_profile.first_name}"
        assert db_test_user_profile.last_name == last_name, \
            f"Expected last_name to be {last_name}, got {db_test_user_profile.last_name}"

        # Test that the Timestamp columns were automatically populated
        assert isinstance(db_test_user_profile.created_at, datetime), \
            f"Expected created_at to be datetime, got {type(db_test_user_profile.created_at)}"
        assert isinstance(db_test_user_profile.updated_at, datetime), \
            f"Expected updated_at to be datetime, got {type(db_test_user_profile.updated_at)}"
        assert db_test_user_profile.created_at == db_test_user_profile.updated_at, \
            "Expected created_at and updated_at to be equal"

        # Delete the user from the database
        db_test_user = db.query(User).filter_by(username=username).first()
        db.delete(db_test_user)
        db.commit()

        # Check that the user profile was automatically deleted
        db_test_user_profile = db.query(UserProfile).filter_by(username=username).first()
        assert db_test_user_profile is None, \
            "Expected user profile to be None"