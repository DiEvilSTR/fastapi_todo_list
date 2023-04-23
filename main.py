import uvicorn

from fastapi import FastAPI

from api.api_v1.api_router import api_router
from core.config import settings
from db.db_setup import engine
from models import user, task

user.Base.metadata.create_all(bind=engine)
task.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version="0.0.1",
    contact={
        "name": settings.AUTHOR,
        "email": settings.AUTHOR_EMAIL,
    }
)

app.include_router(api_router, prefix=settings.API_V1_STR)