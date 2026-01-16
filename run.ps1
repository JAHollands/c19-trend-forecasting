# run.ps1
# MVP bootstrap + run script (Windows PowerShell)

$ErrorActionPreference = "Stop"

# Repo root = folder this script sits in
$repoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path

$venvPath  = Join-Path $repoRoot ".venv"
$pythonExe = Join-Path $venvPath "Scripts\python.exe"

# 1) Create venv if missing
if (!(Test-Path $pythonExe)) {
    Write-Host "Creating virtual environment at .venv ..."
    python -m venv $venvPath
}

# 2) Install dependencies
Write-Host "Installing requirements..."
& $pythonExe -m pip install --upgrade pip
& $pythonExe -m pip install -r (Join-Path $repoRoot "requirements.txt")

# 3) Run pipeline
Write-Host "Running pipeline..."
Set-Location $repoRoot
& $pythonExe -m src.pipeline