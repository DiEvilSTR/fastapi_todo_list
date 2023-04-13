# The function of this file is to check whether the request is authorized or not [Verification of the protected route]
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .jwt_handler import decode_jwt

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)


    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication scheme!"
                )
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token or expired token.")
            # request.state.username = decode_jwt(credentials.credentials)["username"]
            return credentials.credentials
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authorization code."
            )


    def verify_jwt(self, jwtoken: str):
        is_token_valid: bool = False # A false flag

        try:
            payload = decode_jwt(jwtoken)
        except:
            payload = None
        
        if payload:
            is_token_valid = True
        return is_token_valid


    @staticmethod
    def get_username(jwtoken: str) -> str:
        try:
            username = decode_jwt(jwtoken)["username"]
        except:
            username = None
        return username
