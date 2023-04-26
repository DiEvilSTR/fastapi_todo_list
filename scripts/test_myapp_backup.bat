@echo off

rem Activate the virtual environment
.\venv\Scripts\activate.bat

rem Run the unit tests
pytest tests/

rem Deactivate the virtual environment
.\venv\Scripts\deactivate.bat