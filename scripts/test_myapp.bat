@echo off

rem Activate the virtual environment
rem ./venv/Scripts/activate.bat

rem Run Alembic migrations
alembic -x test=true revision --autogenerate -m "Test migrations"
alembic -x test=true upgrade head

rem Run the unit tests
pytest -v tests/unit/api/

rem Run the integration tests
pytest -v tests/integration/models/

rem Run the system tests
pytest -v tests/system/

rem Deactivate the virtual environment
rem ./venv/Scripts/deactivate.bat