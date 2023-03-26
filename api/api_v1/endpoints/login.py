from fastapi import Body, APIRouter, HTTPException, status

from crud.crud_user import authenticate
from schemas.user import UserLoginSchema
from core.jwt_authentication.jwt_handler import sign_jwt


router = APIRouter()


@router.post("/login")
def user_login(user: UserLoginSchema = Body(default=None)):

    if authenticate():
        return sign_jwt(user.email)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login details!"
        )
