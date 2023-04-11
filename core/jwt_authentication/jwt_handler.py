# This file is responsible for sighing, encoding, decoding and returning JWTs.
import time
import jwt

from decouple import config

JWT_SECRET_KEY = config("SECRET_KEY")
JWT_ALGORITHM = config("ALGORITHM")

token_lifespan = 600


# Function returns the generated Tokens (JWTs)
def token_response(token: str):
    return {
        "access token": token,
        "token_type": "bearer"
    }


# Function used for signing the JWT string
def sign_jwt(userID: str):
    payload = {
        "userID": userID,
        "expires": time.time() + token_lifespan
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decode_jwt(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return decode_token if decode_token["expires"] >= time.time() else None
    except:
        return {}
