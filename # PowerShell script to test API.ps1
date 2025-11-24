# PowerShell script to test API

Write-Host "======================================================================"
Write-Host "API Testing Script" -ForegroundColor Cyan
Write-Host "======================================================================"

# Check if server is running
Write-Host "`nChecking if API server is running..." -ForegroundColor Yellow
try {
    $health = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -ErrorAction Stop
    Write-Host "✓ Server is running" -ForegroundColor Green
    Write-Host "  Status: $($health.status)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Server is not running!" -ForegroundColor Red
    Write-Host "`nPlease start the server first:" -ForegroundColor Yellow
    Write-Host "  python start_api.py" -ForegroundColor White
    exit 1
}

# Test 1: Root endpoint
Write-Host "`n[1/4] Testing root endpoint..." -ForegroundColor Yellow
try {
    $root = Invoke-RestMethod -Uri "http://localhost:8000/" -Method Get
    Write-Host "✓ Root endpoint working" -ForegroundColor Green
    Write-Host "  Message: $($root.message)" -ForegroundColor Gray
} catch {
    Write-Host "❌ Failed: $_" -ForegroundColor Red
}

# Test 2: Single prediction (non-smoker)
Write-Host "`n[2/4] Testing single prediction (non-smoker)..." -ForegroundColor Yellow
$body1 = @{
    age = 35
    sex = "male"
    bmi = 27.5
    children = 2
    smoker = "no"
    region = "northwest"
} | ConvertTo-Json

try {
    $prediction1 = Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -Body $body1 -ContentType "application/json"
    Write-Host "✓ Prediction successful" -ForegroundColor Green
    Write-Host "  Predicted Cost: `$$([math]::Round($prediction1.predicted_cost, 2))" -ForegroundColor Gray
} catch {
    Write-Host "❌ Failed: $_" -ForegroundColor Red
}

# Test 3: Single prediction (smoker)
Write-Host "`n[3/4] Testing single prediction (smoker)..." -ForegroundColor Yellow
$body2 = @{
    age = 35
    sex = "male"
    bmi = 27.5
    children = 2
    smoker = "yes"
    region = "northwest"
} | ConvertTo-Json

try {
    $prediction2 = Invoke-RestMethod -Uri "http://localhost:8000/predict" -Method Post -Body $body2 -ContentType "application/json"
    Write-Host "✓ Prediction successful" -ForegroundColor Green
    Write-Host "  Predicted Cost: `$$([math]::Round($prediction2.predicted_cost, 2))" -ForegroundColor Gray
    Write-Host "  Note: Smokers typically have higher costs" -ForegroundColor Gray
} catch {
    Write-Host "❌ Failed: $_" -ForegroundColor Red
}

# Test 4: Batch prediction
Write-Host "`n[4/4] Testing batch prediction..." -ForegroundColor Yellow
$batchBody = @(
    @{
        age = 25
        sex = "female"
        bmi = 22.5
        children = 0
        smoker = "no"
        region = "northeast"
    },
    @{
        age = 45
        sex = "male"
        bmi = 30.0
        children = 2
        smoker = "yes"
        region = "southeast"
    }
) | ConvertTo-Json

try {
    $batchResult = Invoke-RestMethod -Uri "http://localhost:8000/batch_predict" -Method Post -Body $batchBody -ContentType "application/json"
    Write-Host "✓ Batch prediction successful" -ForegroundColor Green
    Write-Host "  Number of predictions: $($batchResult.count)" -ForegroundColor Gray
    for ($i = 0; $i -lt $batchResult.predictions.Count; $i++) {
        Write-Host "  Patient $($i+1): `$$([math]::Round($batchResult.predictions[$i], 2))" -ForegroundColor Gray
    }
} catch {
    Write-Host "❌ Failed: $_" -ForegroundColor Red
}

Write-Host "`n======================================================================" -ForegroundColor Cyan
Write-Host "API Testing Complete!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Cyan