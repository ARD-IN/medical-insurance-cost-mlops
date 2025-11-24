"""
Setup script to prepare environment for testing
"""
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"{description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print(f"Output: {e.stdout}")
        print(f"Error: {e.stderr}")
        return False

def main():
    """Main setup function"""
    print("Setting up environment for testing...")
    
    # Check if data exists
    data_file = Path("data/raw/insurance.csv")
    if not data_file.exists():
        print("\n⚠️  Data not found. Please run data download first.")
        print("Options:")
        print("1. python download_data.py")
        print("2. python download_data_alternative.py")
        print("3. python download_data_manual.py")
        return False
    
    # Run preprocessing
    if not Path("data/processed/X_train.csv").exists():
        if not run_command("python src/data/preprocess.py", "Running preprocessing..."):
            return False
    
    # Run training
    if not Path("models/model.pkl").exists():
        if not run_command("python src/models/train.py", "Training models..."):
            return False
    
    print("\n" + "="*60)
    print("✓ Setup complete! You can now run tests.")
    print("="*60)
    print("\nRun tests with: pytest tests/ -v")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)