# Setup Script for Portfolio Project
# Run this after cloning the repository

Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Portfolio Project Setup" -ForegroundColor Cyan
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "✓ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✓ Virtual environment already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host ""
Write-Host "Creating .env file from example..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "✓ .env file created - Please update with your settings" -ForegroundColor Green
} else {
    Write-Host "! .env file already exists" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Running migrations..." -ForegroundColor Yellow
python manage.py makemigrations
python manage.py migrate

Write-Host ""
Write-Host "Creating logs directory..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "logs" | Out-Null
Write-Host "✓ Logs directory created" -ForegroundColor Green

Write-Host ""
Write-Host "Creating media directory..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path "media" | Out-Null
Write-Host "✓ Media directory created" -ForegroundColor Green

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Update .env file with your settings" -ForegroundColor White
Write-Host "2. Create a superuser: python manage.py createsuperuser" -ForegroundColor White
Write-Host "3. Run the development server: python manage.py runserver" -ForegroundColor White
Write-Host "4. Access admin panel at: http://127.0.0.1:8000/admin/" -ForegroundColor White
Write-Host "5. (Optional) Sync GitHub projects: python manage.py sync_github" -ForegroundColor White
Write-Host ""

