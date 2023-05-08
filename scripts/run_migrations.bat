@echo off

rem Run Alembic migrations
alembic revision --autogenerate -m "Initial migrations"
alembic upgrade head