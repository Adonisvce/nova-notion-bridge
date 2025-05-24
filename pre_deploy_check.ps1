Write-Host "🔍 Checking requirements.txt for issues..." -ForegroundColor Cyan

$path = "requirements.txt"
if (-Not (Test-Path $path)) {
    Write-Host "❌ requirements.txt not found." -ForegroundColor Red
    exit 1
}

$lines = Get-Content $path | Where-Object { $_ -match '\S' } # Remove empty lines
$seen = @{}
$errors = 0

foreach ($line in $lines) {
    $package = $line.Trim()
    
    if ($seen.ContainsKey($package)) {
        Write-Host "⚠️ Duplicate found: $package" -ForegroundColor Yellow
        $errors++
    } else {
        $seen[$package] = $true
        $pkgName = $package.Split('=')[0] # Support version pinning like package==1.2.3
        $pkgCheck = pip show $pkgName 2>$null

        if (-Not $pkgCheck) {
            Write-Host "❌ Package missing: $pkgName" -ForegroundColor Red
            $errors++
        }
    }
}

if ($errors -eq 0) {
    Write-Host "✅ All packages are valid and no duplicates found." -ForegroundColor Green
    exit 0
} else {
    Write-Host "⚠️ $errors issue(s) found. Please fix before deploy." -ForegroundColor Yellow
    exit 1
}
