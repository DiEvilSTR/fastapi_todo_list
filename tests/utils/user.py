from typing import Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from core.config import settings
from crud import crud_user
from models.user import User
from schemas.user import UserCreate, UserUpdate
from tests.utils.utils import random_lower_string


def user_authentication_headers(*, client: TestClient, username: str, password: str) -> Dict[str, str]:
    data = {"username": username, "password": password}

    r = client.post(f"{settings.API_V1_STR}/login/", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def create_random_user(db: Session) -> User:
    username = random_lower_string()
    password = random_lower_string()
    user_in = UserCreate(username=username, password=password)
    test_user = crud_user.create_user(db=db, obj_in=user_in)
    return test_user