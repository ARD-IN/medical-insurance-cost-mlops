"""
Manual download instructions and sample data creator
"""
import pandas as pd
import numpy as np
from pathlib import Path

def create_sample_data():
    """Create sample dataset for testing if download fails"""
    print("\n⚠️  Creating sample dataset for testing...")
    
    # Generate sample data
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'age': np.random.randint(18, 65, n_samples),
        'sex': np.random.choice(['male', 'female'], n_samples),
        'bmi': np.random.uniform(15, 45, n_samples),
        'children': np.random.randint(0, 5, n_samples),
        'smoker': np.random.choice(['yes', 'no'], n_samples),
        'region': np.random.choice(['northeast', 'northwest', 'southeast', 'southwest'], n_samples)
    }
    
    # Create realistic charges based on features
    charges = (
        data['age'] * 250 +
        data['bmi'] * 350 +
        data['children'] * 500 +
        (data['smoker'] == 'yes').astype(int) * 20000 +
        np.random.normal(3000, 5000, n_samples)
    )
    data['charges'] = np.maximum(charges, 1000)  # Minimum charge
    
    df = pd.DataFrame(data)
    
    # Save to data/raw
    raw_dir = Path("data/raw")
    raw_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = raw_dir / "insurance.csv"
    df.to_csv(output_file, index=False)
    
    print(f"✓ Sample data created: {output_file}")
    print(f"  Samples: {len(df)}")
    print(f"  Columns: {df.columns.tolist()}")
    
    return output_file

def show_manual_instructions():
    """Show manual download instructions"""
    print("\n" + "="*70)
    print("MANUAL DOWNLOAD INSTRUCTIONS")
    print("="*70)
    print("\nIf automatic download fails, follow these steps:")
    print("\n1. Go to: https://www.kaggle.com/datasets/mosapabdelghany/medical-insurance-cost-dataset")
    print("\n2. Click 'Download' button (you may need to sign in)")
    print("\n3. Extract the ZIP file")
    print("\n4. Copy the CSV file to:")
    print(f"   C:\\Users\\SSIASDE\\Workspace\\medical_insurance_cost\\data\\raw\\")
    print("\n5. The file should be named: insurance.csv")
    print("="*70)

def main():
    """Main function"""
    print("\n" + "="*70)
    print("Medical Insurance Dataset - Manual Setup")
    print("="*70)
    
    show_manual_instructions()
    
    print("\n\nOptions:")
    print("1. Download manually and place in data/raw/")
    print("2. Use sample data for testing")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "2":
        create_sample_data()
        print("\n✓ You can now continue with data preprocessing!")
        print("  Run: python src\\data\\preprocess.py")
    else:
        print("\n⏳ Waiting for manual download...")
        print("After downloading, run: python src\\data\\preprocess.py")

if __name__ == "__main__":
    main()