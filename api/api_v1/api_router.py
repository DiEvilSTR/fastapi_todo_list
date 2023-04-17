from fastapi import APIRouter

from .endpoints import login, tasks, users

api_router = APIRouter()

api_router.include_router(login.router, tags=["users"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(users.router, prefix="/users", tags=["users"])