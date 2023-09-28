@echo off
echo on
py -m venv venv
call venv\Scripts\activate.bat
py -m pip install --upgrade pip
pip install poetry
poetry install
.\prestart.sh && uvicorn --host=0.0.0.0 --port=4001 app.main:app --reload