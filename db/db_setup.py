from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from core.config import settings



engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    connect_args={},
    future=True
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    future=True
)

Base = declarative_base()

# DB Utilities
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()