@echo off

rem Activate the virtual environment
./venv/Scripts/activate.bat

rem Run Alembic migrations
alembic -x test=true revision --autogenerate -m "Test migrations"
alembic -x test=true upgrade head

rem Run the unit tests
./scripts/test_myapp_unit.bat

rem Deactivate the virtual environment
./venv/Scripts/deactivate.bat