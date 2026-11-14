#!/bin/sh
# macOS / Linux: sets up a local environment on first run, then starts the app.
cd "$(dirname "$0")" || exit 1
if [ ! -d .venv ]; then
    python3 -m venv .venv || exit 1
    .venv/bin/python -m pip install --upgrade pip
    .venv/bin/python -m pip install -r requirements.txt || exit 1
fi
exec .venv/bin/python -m streamlit run app.py
