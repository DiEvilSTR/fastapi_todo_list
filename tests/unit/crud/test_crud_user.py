import pytest
from crud.crud_user import get_user
from tests.conftest import get_test_db
from api.api_v1.endpoints.users import read_user

def mock_get_user(db, username):
    return {"username": username, "hashed_password": "test_password", "is_active": False, "profile": None}


def test_read_user(monkeypatch):
    monkeypatch.setattr("crud.crud_user.get_user", mock_get_user)
    response = read_user("test_username", get_test_db())
    assert response == {"username": "test_username", "hashed_password": "test_password", "is_active": False, "profile": None}