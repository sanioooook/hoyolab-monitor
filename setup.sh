#!/usr/bin/env bash
set -e

echo "[Setup] Installing dependencies..."
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    echo "[Setup] Creating .env from template..."
    cp .env.example .env
    echo "[Setup] Open .env and fill in your credentials, then run: python main.py"
else
    echo "[Setup] .env already exists, skipping."
    echo "[Setup] Done. Run: python main.py"
fi
