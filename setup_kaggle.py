"""
Helper script to setup Kaggle credentials
"""
import os
import json
from pathlib import Path

def setup_kaggle():
    """Interactive Kaggle credentials setup"""
    print("\n" + "="*70)
    print("KAGGLE CREDENTIALS SETUP")
    print("="*70)
    
    kaggle_dir = Path.home() / ".kaggle"
    kaggle_json = kaggle_dir / "kaggle.json"
    
    if kaggle_json.exists():
        print("\n✓ Kaggle credentials already exist!")
        print(f"Location: {kaggle_json}")
        
        choice = input("\nDo you want to update credentials? (y/n): ").strip().lower()
        if choice != 'y':
            return True
    
    print("\n" + "-"*70)
    print("To get your Kaggle credentials:")
    print("1. Go to: https://www.kaggle.com/account")
    print("2. Scroll to 'API' section")
    print("3. Click 'Create New Token'")
    print("4. A file 'kaggle.json' will be downloaded")
    print("-"*70)
    
    print("\nEnter your Kaggle credentials:")
    username = input("Kaggle Username: ").strip()
    key = input("Kaggle Key: ").strip()
    
    if not username or not key:
        print("\n❌ Username and key cannot be empty!")
        return False
    
    # Create .kaggle directory
    kaggle_dir.mkdir(exist_ok=True)
    
    # Create kaggle.json
    credentials = {
        "username": username,
        "key": key
    }
    
    with open(kaggle_json, 'w') as f:
        json.dump(credentials, f, indent=2)
    
    # Set permissions (Unix-like systems)
    if os.name != 'nt':
        os.chmod(kaggle_json, 0o600)
    
    print(f"\n✓ Credentials saved to: {kaggle_json}")
    print("✓ You can now download datasets from Kaggle!")
    
    return True

if __name__ == "__main__":
    if setup_kaggle():
        print("\n" + "="*70)
        print("✓ Setup complete!")
        print("="*70)
        print("\nNow run: python download_data.py")
    else:
        print("\n❌ Setup failed!")