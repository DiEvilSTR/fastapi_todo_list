from decouple import config
from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserCreate

PASSWORD_HASH = config('PASSWORD_HASH')

def get_user(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate):
    fake_hashed_password = user.password + PASSWORD_HASH
    db_user = User(username=user.username, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate(db: Session, username: str, password: str):
    hashed_entered_password = password + PASSWORD_HASH
    db_user = get_user(db, username=username)
    if not db_user:
        return None
    if not hashed_entered_password == db_user.hashed_password:
        return None
    return db_user