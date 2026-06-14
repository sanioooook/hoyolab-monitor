@echo off
echo [Setup] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [Error] pip install failed. Make sure Python 3.10+ is installed.
    pause
    exit /b 1
)

if not exist .env (
    echo [Setup] Creating .env from template...
    copy .env.example .env
    echo [Setup] Open .env and fill in your credentials, then run: python main.py
) else (
    echo [Setup] .env already exists, skipping.
    echo [Setup] Done. Run: python main.py
)
pause
