# Developer Guide

## Setting Up Development Environment

### 1. Clone and Setup

```bash
cd C:\Users\SSIASDE\Workspace\medical_insurance_cost

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Install dev dependencies
pip install black flake8 mypy pytest-watch
```

### 2. IDE Configuration

#### VS Code
Create `.vscode/settings.json`:
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe",
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "python.testing.pytestEnabled": true,
  "python.testing.unittestEnabled": false
}
```

## Code Style Guide

### Python Style (PEP 8)

```python
# Use descriptive variable names
age_in_years = 35  # Good
a = 35  # Bad

# Function docstrings
def predict_cost(features: dict) -> float:
    """
    Predict insurance cost based on features.
    
    Args:
        features: Dictionary containing patient information
        
    Returns:
        Predicted insurance cost in USD
    """
    pass

# Type hints
def process_data(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Process raw data"""
    pass
```

### Code Formatting

```bash
# Format code with black
black src/ tests/

# Check with flake8
flake8 src/ tests/ --max-line-length=100

# Type checking
mypy src/
```

## Project Structure

```
src/
├── data/           # Data processing
│   ├── __init__.py
│   └── preprocess.py
├── models/         # Model training & evaluation
│   ├── __init__.py
│   ├── train.py
│   └── evaluate.py
└── api/           # API endpoints
    ├── __init__.py
    └── app.py
```

## Adding New Features

### 1. Add New Model

```python
# src/models/train.py

def train_new_model(X_train, y_train, config):
    """Train new model"""
    from sklearn.neural_network import MLPRegressor
    
    params = config['model']['mlp']
    model = MLPRegressor(**params)
    model.fit(X_train, y_train)
    
    return model, params
```

### 2. Add New API Endpoint

```python
# src/api/app.py

@app.post("/predict_with_confidence")
async def predict_with_confidence(features: InsuranceFeatures):
    """Predict with confidence interval"""
    # Implementation
    pass
```

### 3. Add Tests

```python
# tests/test_new_feature.py

def test_new_model():
    """Test new model training"""
    # Implementation
    pass

def test_new_endpoint():
    """Test new API endpoint"""
    response = client.post("/predict_with_confidence", json=test_data)
    assert response.status_code == 200
```

## Testing

### Run Tests

```bash
# All tests
pytest tests/ -v

# Specific test file
pytest tests/test_api.py -v

# With coverage
pytest tests/ --cov=src --cov-report=html

# Watch mode (auto-rerun on changes)
pytest-watch
```

### Writing Tests

```python
import pytest
from fastapi.testclient import TestClient

@pytest.fixture
def client():
    """Create test client"""
    from src.api.app import app
    return TestClient(app)

def test_prediction(client):
    """Test prediction endpoint"""
    response = client.post("/predict", json={
        "age": 35,
        "sex": "male",
        "bmi": 27.5,
        "children": 2,
        "smoker": "no",
        "region": "northwest"
    })
    assert response.status_code == 200
    assert "predicted_cost" in response.json()
```

## Debugging

### Using pdb

```python
import pdb

def problematic_function():
    # Set breakpoint
    pdb.set_trace()
    # Code to debug
```

### Logging

```python
import logging

logger = logging.getLogger(__name__)

def process_data(df):
    logger.info(f"Processing {len(df)} records")
    logger.debug(f"Columns: {df.columns.tolist()}")
    # Processing logic
```

## Performance Optimization

### Profiling

```python
# Profile code
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Code to profile
train_model()

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

### Optimization Tips

1. **Use vectorized operations**
```python
# Good
df['age_squared'] = df['age'] ** 2

# Bad
df['age_squared'] = df['age'].apply(lambda x: x ** 2)
```

2. **Cache expensive computations**
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def expensive_computation(param):
    # Expensive operation
    pass
```

## Git Workflow

### Branch Strategy

```bash
main          # Production-ready code
├── develop   # Integration branch
    ├── feature/new-model      # Feature branches
    ├── feature/api-endpoint
    └── bugfix/prediction-error  # Bug fixes
```

### Commit Messages

```bash
# Format
<type>: <subject>

<body>

<footer>

# Example
feat: Add XGBoost model training

Implement XGBoost model with hyperparameter tuning.
Achieved R² score of 0.88 on test set.

Closes #123
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

## CI/CD Pipeline

### GitHub Actions Example

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        pytest tests/ --cov=src
    
    - name: Lint
      run: |
        flake8 src/ tests/
```

## Troubleshooting

### Common Issues

1. **Import errors**
```python
# Add to sys.path
import sys
sys.path.insert(0, '/path/to/project')
```

2. **Model loading issues**
```python
# Check file existence
from pathlib import Path
model_path = Path("models/model.pkl")
assert model_path.exists(), f"Model not found at {model_path}"
```

3. **Memory issues**
```python
# Use generators for large datasets
def data_generator(file_path, chunk_size=1000):
    for chunk in pd.read_csv(file_path, chunksize=chunk_size):
        yield chunk
```

## Best Practices

1. ✅ Write tests for new features
2. ✅ Document functions with docstrings
3. ✅ Use type hints
4. ✅ Follow PEP 8 style guide
5. ✅ Keep functions small and focused
6. ✅ Use meaningful variable names
7. ✅ Handle exceptions gracefully
8. ✅ Log important events
9. ✅ Version control everything
10. ✅ Review code before committing