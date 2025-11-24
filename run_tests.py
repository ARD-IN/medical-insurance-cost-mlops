"""
Complete test runner with setup
"""
import subprocess
import sys
from pathlib import Path
import os

def check_data_exists():
    """Check if raw data exists"""
    data_file = Path("data/raw/insurance.csv")
    return data_file.exists()

def check_processed_data():
    """Check if processed data exists"""
    files = [
        "data/processed/X_train.csv",
        "data/processed/X_test.csv",
        "data/processed/scaler.pkl",
        "data/processed/label_encoders.pkl"
    ]
    return all(Path(f).exists() for f in files)

def check_model_exists():
    """Check if model exists"""
    return Path("models/model.pkl").exists()

def run_command(cmd):
    """Run command and return success status"""
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        if e.stdout:
            print(f"Output: {e.stdout}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return False

def setup_environment():
    """Setup environment for testing"""
    print("\n" + "="*60)
    print("Setting up test environment...")
    print("="*60)
    
    # Check raw data
    if not check_data_exists():
        print("\n❌ Raw data not found!")
        print("Please run one of:")
        print("  - python download_data.py")
        print("  - python download_data_manual.py (option 2 for sample data)")
        return False
    print("✓ Raw data found")
    
    # Run preprocessing if needed
    if not check_processed_data():
        print("\nRunning preprocessing...")
        if not run_command(f"{sys.executable} src/data/preprocess.py"):
            print("❌ Preprocessing failed!")
            return False
        print("✓ Preprocessing completed")
    else:
        print("✓ Processed data found")
    
    # Run training if needed
    if not check_model_exists():
        print("\nTraining model...")
        if not run_command(f"{sys.executable} src/models/train.py"):
            print("❌ Training failed!")
            return False
        print("✓ Model trained")
    else:
        print("✓ Model found")
    
    return True

def run_tests():
    """Run pytest with proper error handling"""
    print("\n" + "="*60)
    print("Running tests...")
    print("="*60 + "\n")
    
    try:
        # Run pytest
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "tests/", "-v", "-s"],
            cwd=os.getcwd()
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error running tests: {e}")
        return False

def main():
    """Main test runner"""
    # Change to script directory
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    print("="*60)
    print("Medical Insurance Cost - Test Runner")
    print("="*60)
    print(f"Working directory: {os.getcwd()}")
    
    # Setup environment
    if not setup_environment():
        print("\n❌ Setup failed! Cannot run tests.")
        return False
    
    # Run tests
    success = run_tests()
    
    print("\n" + "="*60)
    if success:
        print("✓ All tests passed!")
    else:
        print("⚠️  Some tests failed or had issues")
    print("="*60)
    
    return success

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest run interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)