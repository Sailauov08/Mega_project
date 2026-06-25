@echo off
cd /d "%~dp0.."
call "%~dp0..\venv\Scripts\activate.bat" 2>nul
if errorlevel 1 (
    echo Using system Python
)
python scripts\nightly_pipeline.py >> logs\nightly.log 2>&1
