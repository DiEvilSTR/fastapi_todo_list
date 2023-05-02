from fastapi import Depends, APIRouter, HTTPException, Response, status
from sqlalchemy.orm import Session

from core.jwt_authentication.jwt_bearer import jwt_scheme
from core.jwt_authentication.jwt_handler import sign_jwt
from crud import crud_user
from db.db_setup import get_db
from schemas.auth import Token
from schemas.login import UserLogin

router = APIRouter()


#1 User Login [Login user]
@router.post("/login", response_model=Token)
def user_login(user: UserLogin, db: Session = Depends(get_db)):
    if crud_user.authenticate(db=db, user=user):
        return sign_jwt(user.username)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login details!"
        )


#2 User Logout [Logout user]
@router.post("/logout", dependencies=[Depends(jwt_scheme)])
def user_logout(response: Response):
    response.delete_cookie(key="Authorization")
    return {"detail": "Successfully logged out!"}
