"""
Script to download medical insurance cost dataset from Kaggle
"""
import kagglehub
import shutil
import os
from pathlib import Path

def setup_kaggle_credentials():
    """Setup Kaggle credentials if not already configured"""
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_json = kaggle_dir / "kaggle.json"
    
    if not kaggle_json.exists():
        print("\n⚠️  Kaggle credentials not found!")
        print("\nPlease follow these steps:")
        print("1. Go to https://www.kaggle.com/account")
        print("2. Scroll to 'API' section")
        print("3. Click 'Create New Token'")
        print("4. Download kaggle.json")
        print(f"5. Place it at: {kaggle_json}")
        print("\nOr set environment variables:")
        print("   KAGGLE_USERNAME=your_username")
        print("   KAGGLE_KEY=your_key")
        return False
    return True

def download_dataset():
    """Download dataset from Kaggle and organize it"""
    
    # Check credentials
    if not setup_kaggle_credentials():
        print("\n❌ Cannot proceed without Kaggle credentials")
        return None
    
    try:
        # Download latest version
        print("Downloading dataset from Kaggle...")
        path = kagglehub.dataset_download("mosapabdelghany/medical-insurance-cost-dataset")
        print(f"✓ Downloaded to: {path}")
        
        # Create data directory structure
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        raw_dir = data_dir / "raw"
        raw_dir.mkdir(exist_ok=True)
        
        # Copy dataset to our project structure
        files_copied = 0
        for file in Path(path).glob("*.csv"):
            dest = raw_dir / file.name
            shutil.copy(file, dest)
            print(f"✓ Copied {file.name} to {dest}")
            files_copied += 1
        
        if files_copied == 0:
            print("\n⚠️  No CSV files found in downloaded dataset")
            print(f"Downloaded path: {path}")
            print("Contents:")
            for item in Path(path).iterdir():
                print(f"  - {item.name}")
            return None
        
        print(f"\n✓ Dataset downloaded and organized successfully!")
        print(f"✓ {files_copied} file(s) copied to {raw_dir}")
        return raw_dir
        
    except Exception as e:
        print(f"\n❌ Error downloading dataset: {e}")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Verify Kaggle credentials are set up correctly")
        print("3. Make sure you have accepted the dataset terms on Kaggle")
        return None

if __name__ == "__main__":
    download_dataset()