import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from api.api_v1.endpoints.users import read_user
from core.config import settings
from crud.crud_user import get_users
from tests.conftest import get_test_db
from tests.utils.utils import random_lower_string
