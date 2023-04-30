import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from api.api_v1.endpoints.users import read_user
from core.config import settings
from crud.crud_user import get_users
from tests.conftest import get_test_db
from tests.utils.utils import random_lower_string

def mock_get_user():
    return {"username": "test_user2", "hashed_password": "test_password", "is_active": False, "profile": None}


def mock_get_users():
    return [{"username": "test_user", "hashed_password": "test_password", "is_active": False, "profile": None}]


def test_read_user(get_test_db, monkeypatch):
    monkeypatch.setattr("crud.crud_user.get_user", mock_get_users())
    response = get_test_db.get(f"{settings.API_V1_STR}/users/")
    assert response == [{"username": "test_user", "hashed_password": "test_password", "is_active": False, "profile": None}]