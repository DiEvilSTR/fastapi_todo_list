@echo off

rem Run Alembic migrations
rem alembic -x test=true revision --autogenerate -m "Test migrations"
rem alembic -x test=true upgrade head 

rem Run the unit tests
pytest tests/unit/api/
