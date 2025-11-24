"""
Model training module with MLflow tracking
"""
import pandas as pd
import numpy as np
import pickle
import yaml
import mlflow
import mlflow.sklearn
from pathlib import Path
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def load_config():
    """Load configuration"""
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def load_processed_data(data_dir):
    """Load preprocessed data"""
    X_train = pd.read_csv(Path(data_dir) / "X_train.csv")
    y_train = pd.read_csv(Path(data_dir) / "y_train.csv").values.ravel()
    X_test = pd.read_csv(Path(data_dir) / "X_test.csv")
    y_test = pd.read_csv(Path(data_dir) / "y_test.csv").values.ravel()
    
    return X_train, y_train, X_test, y_test

def train_model(model_name, X_train, y_train, config):
    """Train a specific model"""
    if model_name == "linear_regression":
        model = LinearRegression()
        params = {}
    elif model_name == "random_forest":
        params = config['model']['random_forest']
        model = RandomForestRegressor(**params)
    elif model_name == "xgboost":
        params = config['model']['xgboost']
        model = XGBRegressor(**params)
    else:
        raise ValueError(f"Unknown model: {model_name}")
    
    model.fit(X_train, y_train)
    return model, params

def evaluate_model(model, X_test, y_test):
    """Evaluate model performance"""
    y_pred = model.predict(X_test)
    
    metrics = {
        "rmse": np.sqrt(mean_squared_error(y_test, y_pred)),
        "mae": mean_absolute_error(y_test, y_pred),
        "r2": r2_score(y_test, y_pred)
    }
    
    return metrics, y_pred

def save_model(model, output_dir):
    """Save trained model"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    with open(output_path / "model.pkl", "wb") as f:
        pickle.dump(model, f)
    
    print(f"Model saved to {output_dir}")

def main():
    """Main training pipeline"""
    config = load_config()
    
    # Setup MLflow
    mlflow.set_experiment(config['mlflow']['experiment_name'])
    mlflow.set_tracking_uri(config['mlflow']['tracking_uri'])
    
    # Load data
    X_train, y_train, X_test, y_test = load_processed_data(config['data']['processed_dir'])
    
    best_model = None
    best_r2 = -float('inf')
    
    # Train all models
    for model_name in config['model']['algorithms']:
        with mlflow.start_run(run_name=model_name):
            print(f"\nTraining {model_name}...")
            
            # Train model
            model, params = train_model(model_name, X_train, y_train, config)
            
            # Evaluate
            metrics, y_pred = evaluate_model(model, X_test, y_test)
            
            # Log to MLflow
            mlflow.log_params(params)
            mlflow.log_metrics(metrics)
            mlflow.sklearn.log_model(model, model_name)
            
            print(f"{model_name} metrics:")
            for metric_name, value in metrics.items():
                print(f"  {metric_name}: {value:.4f}")
            
            # Track best model
            if metrics['r2'] > best_r2:
                best_r2 = metrics['r2']
                best_model = model
                best_model_name = model_name
    
    # Save best model
    save_model(best_model, "models")
    
    # Save metrics
    metrics_dir = Path("metrics")
    metrics_dir.mkdir(exist_ok=True)
    
    import json
    with open(metrics_dir / "metrics.json", "w") as f:
        json.dump({
            "best_model": best_model_name,
            "best_r2": best_r2
        }, f, indent=2)
    
    print(f"\n✓ Training completed! Best model: {best_model_name} (R² = {best_r2:.4f})")

if __name__ == "__main__":
    main()