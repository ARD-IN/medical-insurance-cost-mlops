"""
Tests for data preprocessing
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path

def test_raw_data_exists(project_root_dir):
    """Test if raw data file exists"""
    data_file = project_root_dir / "data" / "raw" / "insurance.csv"
    assert data_file.exists(), "Raw data file not found. Run download_data.py first."

def test_data_can_be_loaded(project_root_dir):
    """Test data can be loaded"""
    data_file = project_root_dir / "data" / "raw" / "insurance.csv"
    
    if not data_file.exists():
        pytest.skip("Raw data not found")
    
    df = pd.read_csv(data_file)
    assert len(df) > 0, "Data file is empty"
    print(f"✓ Loaded {len(df)} rows")

def test_required_columns(project_root_dir):
    """Test required columns exist"""
    data_file = project_root_dir / "data" / "raw" / "insurance.csv"
    
    if not data_file.exists():
        pytest.skip("Raw data not found")
    
    df = pd.read_csv(data_file)
    required_columns = ['age', 'sex', 'bmi', 'children', 'smoker', 'region', 'charges']
    
    for col in required_columns:
        assert col in df.columns, f"Required column '{col}' not found"
    
    print(f"✓ All required columns present: {required_columns}")

def test_data_quality(project_root_dir):
    """Test data quality"""
    data_file = project_root_dir / "data" / "raw" / "insurance.csv"
    
    if not data_file.exists():
        pytest.skip("Raw data not found")
    
    df = pd.read_csv(data_file)
    
    # Check for missing values
    missing = df.isnull().sum().sum()
    assert missing == 0, f"Data contains {missing} missing values"
    
    # Check age range
    assert df['age'].min() >= 0, "Age cannot be negative"
    assert df['age'].max() <= 120, "Age seems unrealistic"
    
    # Check BMI range
    assert df['bmi'].min() > 0, "BMI must be positive"
    assert df['bmi'].max() < 100, "BMI seems unrealistic"
    
    # Check charges are positive
    assert df['charges'].min() >= 0, "Charges cannot be negative"
    
    print(f"✓ Data quality checks passed")
    print(f"  - Age range: {df['age'].min()} - {df['age'].max()}")
    print(f"  - BMI range: {df['bmi'].min():.2f} - {df['bmi'].max():.2f}")
    print(f"  - Charges range: ${df['charges'].min():.2f} - ${df['charges'].max():.2f}")

def test_processed_data_exists(project_root_dir):
    """Test if processed data files exist"""
    processed_dir = project_root_dir / "data" / "processed"
    
    if not processed_dir.exists():
        pytest.skip("Processed data directory not found")
    
    required_files = ['X_train.csv', 'X_test.csv', 'y_train.csv', 'y_test.csv']
    existing_files = []
    
    for file in required_files:
        file_path = processed_dir / file
        if file_path.exists():
            existing_files.append(file)
    
    if len(existing_files) == len(required_files):
        print(f"✓ All processed data files exist")
    else:
        pytest.skip(f"Only {len(existing_files)}/{len(required_files)} processed files found")