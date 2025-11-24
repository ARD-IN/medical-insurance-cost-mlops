"""
Data preprocessing module for medical insurance dataset
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import yaml
import pickle
from pathlib import Path

def load_config():
    """Load configuration from config.yaml"""
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def load_data(raw_dir):
    """Load raw data from CSV"""
    csv_files = list(Path(raw_dir).glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {raw_dir}")
    
    df = pd.read_csv(csv_files[0])
    print(f"Loaded data with shape: {df.shape}")
    print(f"\nColumns: {df.columns.tolist()}")
    return df

def preprocess_data(df, config):
    """Preprocess the dataset"""
    # Handle missing values
    df = df.dropna()
    
    # Encode categorical variables
    label_encoders = {}
    for col in config['features']['categorical']:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col])
            label_encoders[col] = le
    
    # Split features and target
    feature_cols = config['features']['numerical'] + config['features']['categorical']
    X = df[feature_cols]
    y = df[config['features']['target']]
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=config['data']['test_size'],
        random_state=config['data']['random_state']
    )
    
    # Scale numerical features
    scaler = StandardScaler()
    numerical_features = config['features']['numerical']
    X_train[numerical_features] = scaler.fit_transform(X_train[numerical_features])
    X_test[numerical_features] = scaler.transform(X_test[numerical_features])
    
    return X_train, X_test, y_train, y_test, scaler, label_encoders

def save_processed_data(X_train, X_test, y_train, y_test, scaler, label_encoders, output_dir):
    """Save processed data and preprocessing objects"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save data
    X_train.to_csv(output_path / "X_train.csv", index=False)
    X_test.to_csv(output_path / "X_test.csv", index=False)
    y_train.to_csv(output_path / "y_train.csv", index=False)
    y_test.to_csv(output_path / "y_test.csv", index=False)
    
    # Save preprocessing objects
    with open(output_path / "scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
    
    with open(output_path / "label_encoders.pkl", "wb") as f:
        pickle.dump(label_encoders, f)
    
    print(f"Processed data saved to {output_dir}")

def main():
    """Main preprocessing pipeline"""
    config = load_config()
    
    # Load raw data
    df = load_data(config['data']['raw_dir'])
    
    # Preprocess
    X_train, X_test, y_train, y_test, scaler, label_encoders = preprocess_data(df, config)
    
    # Save processed data
    save_processed_data(
        X_train, X_test, y_train, y_test, 
        scaler, label_encoders,
        config['data']['processed_dir']
    )
    
    print("\nPreprocessing completed!")
    print(f"Training samples: {len(X_train)}")
    print(f"Testing samples: {len(X_test)}")

if __name__ == "__main__":
    main()