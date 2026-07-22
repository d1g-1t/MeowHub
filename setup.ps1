param(
    [switch]$SkipBuild
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    $secret = [Convert]::ToBase64String((1..64 | ForEach-Object { Get-Random -Maximum 256 }))
    (Get-Content .env) -replace 'replace-me', $secret | Set-Content .env
    Write-Host ".env created with generated SECRET_KEY" -ForegroundColor Green
}

if (-not $SkipBuild) {
    Write-Host "Building and starting containers..." -ForegroundColor Cyan
    docker compose up -d --build
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERROR: docker compose failed. Is Docker running?" -ForegroundColor Red
        exit 1
    }
}

Write-Host "Running migrations..." -ForegroundColor Cyan
docker compose exec -T api python manage.py migrate

Write-Host ""
Write-Host "Setup complete!" -ForegroundColor Green
Write-Host "  Frontend: http://localhost:3000" -ForegroundColor White
Write-Host "  API:      http://localhost:8000/api/" -ForegroundColor White
Write-Host "  Admin:    http://localhost:8000/admin/" -ForegroundColor White
