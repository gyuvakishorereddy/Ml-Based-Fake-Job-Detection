# Quick Start Script for Windows PowerShell
# Run this script to set up and start both backend and frontend

Write-Host "================================" -ForegroundColor Cyan
Write-Host "   ML Scam Detection System    " -ForegroundColor Cyan
Write-Host "   React + Flask Setup          " -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is installed
Write-Host "Checking Python installation..." -ForegroundColor Yellow
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonVersion = python --version
    Write-Host "✓ $pythonVersion found" -ForegroundColor Green
} else {
    Write-Host "✗ Python not found. Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

# Check if Node.js is installed
Write-Host "Checking Node.js installation..." -ForegroundColor Yellow
if (Get-Command node -ErrorAction SilentlyContinue) {
    $nodeVersion = node --version
    Write-Host "✓ Node.js $nodeVersion found" -ForegroundColor Green
} else {
    Write-Host "✗ Node.js not found. Please install Node.js 16+" -ForegroundColor Red
    exit 1
}

# Ask user what to do
Write-Host ""
Write-Host "What would you like to do?" -ForegroundColor Cyan
Write-Host "1. First-time setup (install dependencies + train models)" -ForegroundColor White
Write-Host "2. Start servers only (skip setup)" -ForegroundColor White
Write-Host "3. Exit" -ForegroundColor White
$choice = Read-Host "Enter your choice (1-3)"

if ($choice -eq "3") {
    exit 0
}

if ($choice -eq "1") {
    Write-Host ""
    Write-Host "======== BACKEND SETUP ========" -ForegroundColor Cyan
    
    # Install Python dependencies
    Write-Host "Installing Python dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to install Python dependencies" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Python dependencies installed" -ForegroundColor Green
    
    # Train models
    Write-Host "Training ML models (this may take 5-15 minutes)..." -ForegroundColor Yellow
    python train_models.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to train models" -ForegroundColor Red
        exit 1
    }
    Write-Host "✓ Models trained successfully" -ForegroundColor Green
    
    Write-Host ""
    Write-Host "======== FRONTEND SETUP ========" -ForegroundColor Cyan
    
    # Install Node dependencies
    Write-Host "Installing Node.js dependencies..." -ForegroundColor Yellow
    Set-Location frontend
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "✗ Failed to install Node dependencies" -ForegroundColor Red
        Set-Location ..
        exit 1
    }
    Write-Host "✓ Node dependencies installed" -ForegroundColor Green
    Set-Location ..
    
    Write-Host ""
    Write-Host "✓ Setup complete!" -ForegroundColor Green
}

Write-Host ""
Write-Host "======== STARTING SERVERS ========" -ForegroundColor Cyan
Write-Host "Backend will run on: http://localhost:5000" -ForegroundColor White
Write-Host "Frontend will run on: http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C in each terminal to stop the servers" -ForegroundColor Yellow
Write-Host ""

# Start backend in new terminal
Write-Host "Starting Flask backend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD'; python app.py"

# Wait a bit for backend to start
Start-Sleep -Seconds 3

# Start frontend in new terminal
Write-Host "Starting React frontend..." -ForegroundColor Yellow
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend'; npm run dev"

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "✓ Both servers starting..." -ForegroundColor Green
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Open your browser and navigate to:" -ForegroundColor Yellow
Write-Host "http://localhost:3000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Check API health at:" -ForegroundColor Yellow
Write-Host "http://localhost:5000/api/health" -ForegroundColor Cyan
Write-Host ""
