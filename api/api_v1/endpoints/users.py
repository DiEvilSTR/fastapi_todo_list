from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.user import User, UserCreate

from crud.crud_user import get_user, get_users, create_user
from db.db_setup import get_db


router = APIRouter()


#1 Read Users [Get list of users]
@router.get("/", response_model=List[User])
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = get_users(db, skip=skip, limit=limit)
    return users


#2 User Signup [Create a new user]
@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
async def user_signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user(db=db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username is already registered."
        )
    create_user(db=db, user=user)
    return db_user


#3 Read User [Get user by username]
@router.get("/user/{username}", response_model=User)
async def read_user(username: str, db: Session = Depends(get_db)):
    db_user = get_user(db=db, username=username)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User with this username does not exists."
        )
    return db_user
