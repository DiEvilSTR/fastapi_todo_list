from fastapi import Depends, APIRouter, HTTPException, status
from sqlalchemy.orm import Session

from core.jwt_authentication.jwt_handler import sign_jwt
from crud.crud_user import authenticate
from db.db_setup import get_db
from schemas.auth import Token
from schemas.login import UserLogin

router = APIRouter()


@router.post("/login", response_model=Token)
def user_login(user: UserLogin, db: Session = Depends(get_db)):
    if authenticate(db=db, user=user):
        return sign_jwt(user.username)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login details!"
        )
