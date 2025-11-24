"""
Alternative script to download dataset using Kaggle API
"""
import os
import zipfile
from pathlib import Path
import subprocess
import sys

def install_kaggle():
    """Install kaggle package if not available"""
    try:
        import kaggle
        print("✓ Kaggle API already installed")
        return True
    except ImportError:
        print("Installing Kaggle API...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle"])
        return True

def setup_kaggle_credentials():
    """Check and setup Kaggle credentials"""
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_json = kaggle_dir / "kaggle.json"
    
    if not kaggle_json.exists():
        print("\n" + "="*60)
        print("⚠️  KAGGLE CREDENTIALS NOT FOUND")
        print("="*60)
        print("\nPlease follow these steps:")
        print("\n1. Go to: https://www.kaggle.com/account")
        print("2. Scroll to 'API' section")
        print("3. Click 'Create New Token'")
        print("4. A file 'kaggle.json' will be downloaded")
        print(f"\n5. Create folder (if not exists): {kaggle_dir}")
        print(f"6. Copy 'kaggle.json' to: {kaggle_json}")
        print("\nAfter placing the file, run this script again.")
        print("="*60)
        return False
    
    # Set correct permissions (Unix-like systems)
    if os.name != 'nt':  # Not Windows
        os.chmod(kaggle_json, 0o600)
    
    print("✓ Kaggle credentials found")
    return True

def download_dataset_kaggle_api():
    """Download dataset using Kaggle API"""
    try:
        from kaggle.api.kaggle_api_extended import KaggleApi
        
        # Initialize API
        api = KaggleApi()
        api.authenticate()
        print("✓ Authenticated with Kaggle")
        
        # Create directories
        data_dir = Path("data")
        raw_dir = data_dir / "raw"
        raw_dir.mkdir(parents=True, exist_ok=True)
        
        # Download dataset
        print("\nDownloading dataset...")
        dataset_name = "mosapabdelghany/medical-insurance-cost-dataset"
        
        api.dataset_download_files(
            dataset_name,
            path=str(raw_dir),
            unzip=True
        )
        
        print(f"✓ Dataset downloaded to {raw_dir}")
        
        # List downloaded files
        print("\nDownloaded files:")
        for file in raw_dir.glob("*"):
            print(f"  - {file.name}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    """Main function"""
    print("="*60)
    print("Medical Insurance Dataset Downloader")
    print("="*60)
    print()
    
    # Install kaggle if needed
    if not install_kaggle():
        print("❌ Failed to install Kaggle API")
        return
    
    # Check credentials
    if not setup_kaggle_credentials():
        return
    
    # Download dataset
    print()
    if download_dataset_kaggle_api():
        print("\n" + "="*60)
        print("✓ SUCCESS! Dataset ready to use")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("❌ Download failed")
        print("="*60)

if __name__ == "__main__":
    main()