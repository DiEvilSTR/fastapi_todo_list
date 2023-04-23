import os
import pytest

from db.db_setup import SessionLocal, Base
from decouple import config
from fastapi import FastAPI
from fastapi.testclient import TestClient
from main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Set up a separate database for testing
TEST_DATABASE_URL = config('TEST_DATABASE_URL')

# Configure the database connection
test_engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Create a new FastAPI application for testing
test_app = FastAPI()

# Override the database dependency in the test environment
@pytest.fixture(autouse=True)
def override_get_db(monkeypatch):
    monkeypatch.setattr("app.dependencies.get_db", lambda: TestingSessionLocal())

# Create a test client for making requests against the application
@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

# Create and drop the test database before and after running the tests
@pytest.fixture(scope="session", autouse=True)
def setup_and_teardown_database():
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)
