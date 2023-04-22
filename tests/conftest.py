import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from decouple import config

from db.db_setup import SessionLocal
from main import app

# Set up a separate database for testing
TEST_DATABASE_URL = config('TEST_DATABASE_URL')

