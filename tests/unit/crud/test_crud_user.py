import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from api.api_v1.endpoints.users import read_user
from core.config import settings
from crud.crud_user import get_user
from tests.conftest import get_test_db
from tests.utils.utils import random_lower_string

def mock_get_user(db, username):
    return {"username": username, "hashed_password": "test_password", "is_active": False, "profile": None}


def test_read_user(get_test_db, monkeypatch):
    username = random_lower_string()
    monkeypatch.setattr("crud.crud_user.get_user", mock_get_user(get_test_db, username))
    response = get_test_db.get(f"{settings.API_V1_STR}/users/{username}")
    assert response == {"username": username, "hashed_password": "test_password", "is_active": False, "profile": None}