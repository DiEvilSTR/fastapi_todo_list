from decouple import config
from sqlalchemy.orm import Session

from core.security import get_password_hash, verify_password
from models.user import User
from schemas.user import UserCreate
from schemas.login import UserLogin


def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate(db: Session, user: UserLogin):
    db_user = get_user(db=db, username=user.username)
    if db_user and verify_password(user.password, db_user.hashed_password):
        return True
    else:
        return None


def delete_user(db: Session, username: str):
    db_user = get_user(db=db, username=username)
    db.delete(db_user)
    db.commit()
    return db_user