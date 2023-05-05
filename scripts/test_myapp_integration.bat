@echo off

rem Run the unit tests
pytest -v tests/integration/crud/
pytest -v tests/integration/models/