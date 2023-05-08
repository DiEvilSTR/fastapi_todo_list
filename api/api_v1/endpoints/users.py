from typing import List

from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session

from core.jwt_authentication.jwt_bearer import jwt_scheme
from crud import crud_user, crud_user_profile
from db import db_setup
from schemas.user import User, UserCreate
from schemas.user_profile import UserProfile, UserProfileUpdate

router = APIRouter()


#1 Read Users [Get list of users]
@router.get("/", response_model=List[User], dependencies=[Depends(jwt_scheme)])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(db_setup.get_db)):
    users = crud_user.get_users(db, skip=skip, limit=limit)
    return users


#2 User Signup [Create a new user]
@router.post("/signup", response_model=User, status_code=status.HTTP_201_CREATED)
def user_signup(user: UserCreate, db: Session = Depends(db_setup.get_db)):
    db_user = crud_user.get_user(db=db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Username is already registered."
        )
    db_user = crud_user.create_user(db=db, user=user)
    crud_user_profile.user_profile_create(db=db, username=user.username)
    return db_user


#3 Read current user [Get current user]
@router.get("/me", response_model=UserProfile, dependencies=[Depends(jwt_scheme)])
def read_current_user(db: Session = Depends(db_setup.get_db), current_user: str = Depends(jwt_scheme)):
    db_user_profile = crud_user_profile.user_profile_get(db=db, username=current_user)
    if db_user_profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User with this username does not exists."
        )
    return db_user_profile


#4 Update User Profile [Update user profile]
@router.patch("/me", response_model=UserProfile, dependencies=[Depends(jwt_scheme)])
def update_user_profile(updated_user_profile: UserProfileUpdate, db: Session = Depends(db_setup.get_db), current_user: str = Depends(jwt_scheme)):
    db_user_profile = crud_user_profile.user_profile_get(db=db, username=current_user)
    if db_user_profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User with this username does not exists."
        )
    db_user_profile = crud_user_profile.user_profile_update(db=db, user_profile=updated_user_profile, username=current_user)
    return db_user_profile


#5 Delete User [Delete user, user profile, and all user's tasks]
@router.delete("/me", dependencies=[Depends(jwt_scheme)])
def delete_user_by_username(response: Response, db: Session = Depends(db_setup.get_db), current_user: str = Depends(jwt_scheme)):
    db_user = crud_user.get_user(db=db, username=current_user)
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User with this username does not exists."
        )
    crud_user.delete_user(db=db, username=current_user)
    response.delete_cookie(key="Authorization")
    return {"detail": f"User {current_user} deleted successfully."}


#6 Read User [Get user by username]
@router.get("/user/{username}", response_model=UserProfile, dependencies=[Depends(jwt_scheme)])
def read_user(username: str, db: Session = Depends(db_setup.get_db)):
    db_user_profile = crud_user_profile.user_profile_get(db=db, username=username)
    if db_user_profile is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User with this username does not exists."
        )
    return db_user_profile



