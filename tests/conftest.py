import os
import pytest
from unittest.mock import patch

from core.config import settings
from db import db_setup
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


# Create a test client for making requests against the application
@pytest.fixture(scope="module")
def get_test_db():
    test_client = TestingSessionLocal()
    try:
        yield test_client
    finally:
        test_client.close()


# Create a test client for making requests against the application
@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as test_client:
        yield test_client


# Create and drop the test database before and after running the tests
@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_database():
    db_setup.Base.metadata.create_all(bind=test_engine)
    yield
    # db_setup.Base.metadata.drop_all(bind=test_engine)
