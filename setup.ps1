Write-Host "[Setup] Installing dependencies..." -ForegroundColor Cyan
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) {
    Write-Host "[Error] pip install failed. Make sure Python 3.10+ is installed." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path ".env")) {
    Write-Host "[Setup] Creating .env from template..." -ForegroundColor Cyan
    Copy-Item ".env.example" ".env"
    Write-Host "[Setup] Open .env and fill in your credentials, then run: python main.py" -ForegroundColor Green
} else {
    Write-Host "[Setup] .env already exists, skipping." -ForegroundColor Yellow
    Write-Host "[Setup] Done. Run: python main.py" -ForegroundColor Green
}
Read-Host "Press Enter to exit"
