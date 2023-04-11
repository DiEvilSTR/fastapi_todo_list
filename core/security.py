from decouple import config

PASSWORD_HASH = config('PASSWORD_HASH')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    fake_hashed_password = plain_password + PASSWORD_HASH
    return hashed_password == fake_hashed_password


def get_password_hash(password: str) -> str:
    fake_hashed_password = password + PASSWORD_HASH
    return fake_hashed_password