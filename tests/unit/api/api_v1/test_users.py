import pytest
from unittest.mock import MagicMock

from crud import crud_user, crud_user_profile

from api.api_v1.endpoints.users import read_user
from core.config import settings
from core.jwt_authentication.jwt_bearer import jwt_scheme
from main import app
from tests.conftest import get_test_db

# Define a test datetime
test_datetime = "2038-01-19T03:14:07.123456"


# Override the JWT scheme dependency in the test environment
def mock_jwt_scheme():
    return "test_user"

app.dependency_overrides[jwt_scheme] = mock_jwt_scheme


def mock_get_user(db, username):
    return None


def mock_get_existing_user(db, username):
    return {"username": "test_user", "is_active": False, "created_at": test_datetime, "updated_at": test_datetime}


def mock_get_users(db, skip, limit):
    return [{"username": "test_user", "is_active": False, "created_at": test_datetime, "updated_at": test_datetime}]


def mock_create_user(db, user):
    return {"username": "test_user", "is_active": False, "created_at": test_datetime, "updated_at": test_datetime}


def mock_user_profile_create(db, username):
    return {"username": "test_user", "is_active": False, "created_at": test_datetime, "updated_at": test_datetime}


# Test the read_user endpoint for calling the crud_user.get_user function
def test_read_users(get_test_db, monkeypatch):
    monkeypatch.setattr(crud_user, "get_users", mock_get_users)
    response = get_test_db.get(f"{settings.API_V1_STR}/users/", headers={"Authorization": "Bearer test_token"})
    mock_get_users.assert_called_once()
    assert response.status_code == 200
    assert response.json() == [{"username": "test_user", "is_active": False, "created_at": test_datetime, "updated_at": test_datetime}]


# Test the signup endpoint for calling the crud_user.create_user function
def test_create_user(get_test_db, monkeypatch):
    monkeypatch.setattr(crud_user, "get_user", mock_get_user)
    monkeypatch.setattr(crud_user, "create_user", mock_create_user)
    monkeypatch.setattr(crud_user_profile, "user_profile_create", mock_user_profile_create)
    response = get_test_db.post(f"{settings.API_V1_STR}/users/signup/", json={"username": "test_user", "password": "test_password"})
    assert response.status_code == 201
    assert response.json() == {"username": "test_user", "is_active": False, "created_at": test_datetime, "updated_at": test_datetime}
