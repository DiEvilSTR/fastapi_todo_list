import os
import pytest

from core.config import settings
from db.db_setup import Base
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker



# Configure the database connection
test_engine = create_engine(
    settings.SQLALCHEMY_TEST_DATABASE_URL,
    connect_args={},
    future=True
    )

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
    future=True
    )


# Override the database dependency in the test environment
@pytest.fixture(autouse=True)
def override_get_db(monkeypatch):
    monkeypatch.setattr("db.db_setup.get_db", lambda: TestingSessionLocal())


# Create a test client for making requests against the application
@pytest.fixture(scope="module")
def get_test_db():
    with TestClient(app) as test_db:
        yield test_db


# Create and drop the test database before and after running the tests
@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
