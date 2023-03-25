import uvicorn

from fastapi import FastAPI

from api.api_v1.api_router import api_router
from db.db_setup import engine
from models import user, task

user.Base.metadata.create_all(bind=engine)
task.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fast API ToDo List",
    description="To Do List manager",
    version="0.0.1",
    contact={
        "name": "DiEvilSTR",
        "email": "dievilstr@gmail.com",
    }
)

app.include_router(api_router, prefix="/api/v1")