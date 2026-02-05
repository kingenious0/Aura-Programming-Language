# Aura Quick Setup Script for Windows
# Run this to add Aura to your PATH automatically

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  AURA GLOBAL SETUP" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Get Python Scripts path
$pythonScripts = python -c "import site; print(site.USER_BASE + '\\Scripts')"

Write-Host "[1/3] Installing Aura globally..." -ForegroundColor Yellow
pip install -e .

Write-Host ""
Write-Host "[2/3] Adding to PATH..." -ForegroundColor Yellow

# Add to current session
$env:Path += ";$pythonScripts"
Write-Host "  ✓ Added to current session" -ForegroundColor Green

# Add permanently
try {
    $currentPath = [Environment]::GetEnvironmentVariable("Path", "User")
    if ($currentPath -notlike "*$pythonScripts*") {
        [Environment]::SetEnvironmentVariable(
            "Path",
            "$currentPath;$pythonScripts",
            "User"
        )
        Write-Host "  ✓ Added to PATH permanently" -ForegroundColor Green
    } else {
        Write-Host "  ✓ Already in PATH" -ForegroundColor Green
    }
} catch {
    Write-Host "  ⚠ Could not add to PATH permanently (need admin)" -ForegroundColor Yellow
    Write-Host "  Run this script as Administrator for permanent PATH" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "[3/3] Testing installation..." -ForegroundColor Yellow

# Test the command
$version = & aura --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ Aura is working!" -ForegroundColor Green
    Write-Host ""
    Write-Host $version -ForegroundColor Cyan
} else {
    Write-Host "  ⚠ Aura command not found" -ForegroundColor Red
    Write-Host "  Please restart your terminal and try: aura --version" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "================================" -ForegroundColor Cyan
Write-Host "  SETUP COMPLETE!" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Try these commands:" -ForegroundColor White
Write-Host "  aura --help        # Show all commands" -ForegroundColor Gray
Write-Host "  aura init          # Create new project" -ForegroundColor Gray
Write-Host "  aura dev           # Start dev server" -ForegroundColor Gray
Write-Host ""
