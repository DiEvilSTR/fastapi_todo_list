from fastapi import Body, APIRouter

from schemas.user import UserSchema
from core.jwt_authentication.jwt_handler import sign_jwt

users = []

router = APIRouter()


#5 User Signup [Create a new user]
@router.post("/user/signup", tags=["users"])
def user_signup(user: UserSchema = Body(default=None)):
    users.append(user)
    return sign_jwt(user.email)
