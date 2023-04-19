# This file is responsible for sighing, encoding, decoding and returning JWTs.
import time
import jwt

from decouple import config

JWT_SECRET_KEY = config("SECRET_KEY")
JWT_ALGORITHM = config("ALGORITHM")

token_lifespan = 60000


# Function used for signing the JWT string
def sign_jwt(username: str):
    payload = {
        "username": username,
        "expires": time.time() + token_lifespan
    }
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return {
        "access_token": token,
        "token_type": "bearer"
    }


# Function used for decoding token
def decode_jwt(token: str):
    try:
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return decoded_token if decoded_token["expires"] >= time.time() else None
    except:
        return None


# Function used for extracting username from token
def extract_username(token: str):
    try:
        return decode_jwt(token)["username"] if decode_jwt(token) else None
    except:
        return None
