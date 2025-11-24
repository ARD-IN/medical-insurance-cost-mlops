"""
Simple direct test without pytest
"""
import sys
from pathlib import Path

def test_data_exists():
    """Test if data exists"""
    print("\n1. Testing data file...")
    data_file = Path("data/raw/insurance.csv")
    if data_file.exists():
        print(f"   ✓ Data file exists: {data_file}")
        return True
    else:
        print(f"   ❌ Data file not found: {data_file}")
        return False

def test_preprocessing():
    """Test preprocessing"""
    print("\n2. Testing preprocessing...")
    files = [
        "data/processed/X_train.csv",
        "data/processed/X_test.csv",
        "data/processed/y_train.csv",
        "data/processed/y_test.csv",
        "data/processed/scaler.pkl",
        "data/processed/label_encoders.pkl"
    ]
    
    all_exist = True
    for file in files:
        file_path = Path(file)
        if file_path.exists():
            print(f"   ✓ {file}")
        else:
            print(f"   ❌ {file}")
            all_exist = False
    
    return all_exist

def test_model():
    """Test model"""
    print("\n3. Testing model...")
    model_file = Path("models/model.pkl")
    if model_file.exists():
        print(f"   ✓ Model file exists: {model_file}")
        return True
    else:
        print(f"   ❌ Model file not found: {model_file}")
        return False

def test_api_import():
    """Test API can be imported"""
    print("\n4. Testing API import...")
    try:
        sys.path.insert(0, str(Path(__file__).parent / "src"))
        from api.app import app
        print("   ✓ API imported successfully")
        return True
    except Exception as e:
        print(f"   ❌ API import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("="*60)
    print("Simple Direct Tests")
    print("="*60)
    
    results = []
    results.append(("Data Exists", test_data_exists()))
    results.append(("Preprocessing", test_preprocessing()))
    results.append(("Model", test_model()))
    results.append(("API Import", test_api_import()))
    
    print("\n" + "="*60)
    print("Test Results:")
    print("="*60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)