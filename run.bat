@echo off
rem Windows: sets up a local environment on first run, then starts the app.
cd /d "%~dp0"
if not exist .venv (
    py -3 -m venv .venv || python -m venv .venv || exit /b 1
    .venv\Scripts\python -m pip install --upgrade pip
    .venv\Scripts\python -m pip install -r requirements.txt || exit /b 1
)
.venv\Scripts\python -m streamlit run app.py
