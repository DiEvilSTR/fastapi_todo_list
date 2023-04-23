from decouple import config
from pydantic import BaseSettings


class Settings(BaseSettings):
    # Project Details
    AUTHOR: str = config("AUTHOR")
    AUTHOR_EMAIL: str = config("AUTHOR_EMAIL")
    PROJECT_NAME: str = config("PROJECT_NAME")
    PROJECT_DESCRIPTION: str = config("PROJECT_DESCRIPTION")
    
    # API V1 url prefix
    API_V1_STR: str = "/api/v1"
    
    # For JWT Authentication
    ALGORITHM: str = config("ALGORITHM")
    SECRET_KEY: str = config("SECRET_KEY")
    
    # Token lifetime: 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    
    # Database url
    SQLALCHEMY_DATABASE_URL = config('DATABASE_URL')
    SQLALCHEMY_TEST_DATABASE_URL = config('TEST_DATABASE_URL')

    class Config:
        case_sensitive = True


settings = Settings()