# PowerShell script for GitHub upload

Write-Host "======================================================================"
Write-Host "GitHub Upload Script" -ForegroundColor Cyan
Write-Host "======================================================================"

# Step 1: Prepare project
Write-Host "`nStep 1: Preparing project..." -ForegroundColor Yellow
python prepare_github.py

# Step 2: Initialize Git (if needed)
if (-not (Test-Path .git)) {
    Write-Host "`nStep 2: Initializing Git..." -ForegroundColor Yellow
    git init
    git branch -M main
} else {
    Write-Host "`nGit already initialized" -ForegroundColor Green
}

# Step 3: Get repository URL
Write-Host "`nStep 3: Repository URL" -ForegroundColor Yellow
$repoUrl = Read-Host "Enter your GitHub repository URL (e.g., https://github.com/username/repo.git)"

if (-not $repoUrl) {
    Write-Host "❌ Repository URL is required" -ForegroundColor Red
    exit 1
}

# Step 4: Add and commit
Write-Host "`nStep 4: Committing files..." -ForegroundColor Yellow
git add .
git commit -m "Initial commit: Medical Insurance Cost MLOps Project"

# Step 5: Add remote and push
Write-Host "`nStep 5: Pushing to GitHub..." -ForegroundColor Yellow
git remote add origin $repoUrl 2>$null
git remote set-url origin $repoUrl
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n======================================================================"
    Write-Host "✓ Successfully uploaded to GitHub!" -ForegroundColor Green
    Write-Host "======================================================================"
    Write-Host "`nRepository: $repoUrl" -ForegroundColor Cyan
} else {
    Write-Host "`n❌ Upload failed" -ForegroundColor Red
    Write-Host "You may need to authenticate with GitHub" -ForegroundColor Yellow
}