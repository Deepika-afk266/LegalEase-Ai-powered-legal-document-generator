@echo off
call .venv\Scripts\activate
set PYTHONPATH=.
pytest -q
