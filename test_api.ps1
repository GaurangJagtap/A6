# PowerShell Test Script for Iris ML REST API
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host " Iris ML Model REST API Test Suite" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# 1. GET /
Write-Host "`n[1] Testing GET http://localhost:5000/" -ForegroundColor Yellow
try {
    $res1 = Invoke-RestMethod -Uri "http://localhost:5000/" -Method GET
    Write-Host "Response:" -ForegroundColor Green
    $res1 | ConvertTo-Json
} catch {
    Write-Host "Failed: $_" -ForegroundColor Red
}

# 2. GET /health
Write-Host "`n[2] Testing GET http://localhost:5000/health" -ForegroundColor Yellow
try {
    $res2 = Invoke-RestMethod -Uri "http://localhost:5000/health" -Method GET
    Write-Host "Response:" -ForegroundColor Green
    $res2 | ConvertTo-Json
} catch {
    Write-Host "Failed: $_" -ForegroundColor Red
}

# 3. POST /predict (Setosa)
Write-Host "`n[3] Testing POST http://localhost:5000/predict (Setosa input)" -ForegroundColor Yellow
try {
    $body3 = '{"features": [5.1, 3.5, 1.4, 0.2]}'
    $res3 = Invoke-RestMethod -Uri "http://localhost:5000/predict" -Method POST -Body $body3 -ContentType "application/json"
    Write-Host "Input: $body3"
    Write-Host "Response:" -ForegroundColor Green
    $res3 | ConvertTo-Json
} catch {
    Write-Host "Failed: $_" -ForegroundColor Red
}

# 4. POST /predict (Versicolor)
Write-Host "`n[4] Testing POST http://localhost:5000/predict (Versicolor input)" -ForegroundColor Yellow
try {
    $body4 = '{"features": [6.0, 2.7, 5.1, 1.6]}'
    $res4 = Invoke-RestMethod -Uri "http://localhost:5000/predict" -Method POST -Body $body4 -ContentType "application/json"
    Write-Host "Input: $body4"
    Write-Host "Response:" -ForegroundColor Green
    $res4 | ConvertTo-Json
} catch {
    Write-Host "Failed: $_" -ForegroundColor Red
}

# 5. POST /predict (Virginica)
Write-Host "`n[5] Testing POST http://localhost:5000/predict (Virginica input)" -ForegroundColor Yellow
try {
    $body5 = '{"features": [6.7, 3.3, 5.7, 2.5]}'
    $res5 = Invoke-RestMethod -Uri "http://localhost:5000/predict" -Method POST -Body $body5 -ContentType "application/json"
    Write-Host "Input: $body5"
    Write-Host "Response:" -ForegroundColor Green
    $res5 | ConvertTo-Json
} catch {
    Write-Host "Failed: $_" -ForegroundColor Red
}

# 6. POST /predict (Invalid Input: 2 features)
Write-Host "`n[6] Testing POST http://localhost:5000/predict (Invalid input: 2 features)" -ForegroundColor Yellow
try {
    $body6 = '{"features": [5.1, 3.5]}'
    $res6 = Invoke-RestMethod -Uri "http://localhost:5000/predict" -Method POST -Body $body6 -ContentType "application/json"
    $res6 | ConvertTo-Json
} catch {
    Write-Host "Expected 400 Bad Request Caught:" -ForegroundColor Green
    Write-Host $_.ErrorDetails.Message
}

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host " API Tests Completed" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

