# pre_deploy_check.ps1
Write-Host "Running pre-deploy validation..."

# Check if requirements.txt exists
if (-Not (Test-Path "requirements.txt")) {
    Write-Host "ERROR: requirements.txt not found." -ForegroundColor Red
    exit 1
}

# Read and validate requirements.txt
$requirements = Get-Content "requirements.txt"
$duplicates = $requirements | Group-Object | Where-Object { $_.Count -gt 1 }

if ($duplicates) {
    Write-Host "ERROR: Duplicate entries found in requirements.txt:" -ForegroundColor Red
    $duplicates | ForEach-Object { Write-Host "  - $($_.Name)" }
    exit 1
}

# Check for known critical packages
$criticalPackages = @("flask", "notion-client", "httpx", "gunicorn", "apscheduler")
foreach ($pkg in $criticalPackages) {
    if (-Not ($requirements -match "^$pkg([=><]|$)")) {
        Write-Host "ERROR: Required package '$pkg' is missing from requirements.txt." -ForegroundColor Red
        exit 1
    }
}

Write-Host "Pre-deploy validation passed. All requirements look good." -ForegroundColor Green
exit 0
