@echo off
echo Starting Smart-Kisan Backend on http://127.0.0.1:8000 ...
cd /d "%~dp0\..\backend"
uv run uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
