@echo off
echo ===================================
echo Medical Insurance MLOps Pipeline
echo ===================================
echo.

echo [1/5] Downloading dataset...
python download_data.py
if errorlevel 1 goto error

echo.
echo [2/5] Preprocessing data...
python src\data\preprocess.py
if errorlevel 1 goto error

echo.
echo [3/5] Training models...
python src\models\train.py
if errorlevel 1 goto error

echo.
echo [4/5] Evaluating model...
python src\models\evaluate.py
if errorlevel 1 goto error

echo.
echo [5/5] Pipeline completed successfully!
echo.
echo You can now:
echo - View MLflow experiments: mlflow ui
echo - Start API server: uvicorn src.api.app:app --reload
echo - Run tests: pytest tests/ -v
echo.
goto end

:error
echo.
echo ERROR: Pipeline failed!
echo.
exit /b 1

:end