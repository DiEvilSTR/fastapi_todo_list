from fastapi import Body, APIRouter, HTTPException, status

from schemas.user import UserLoginSchema
from core.jwt_authentication.jwt_handler import sign_jwt


users = []

router = APIRouter()

def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
        return False


@router.post("/user/login", tags=["user"])
def user_login(user: UserLoginSchema = Body(default=None)):
    if check_user(user):
        return sign_jwt(user.email)
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid login details!"
        )
