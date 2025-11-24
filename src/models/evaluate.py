"""
Model evaluation and visualization module
"""
import pandas as pd
import numpy as np
import pickle
import json
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import yaml

def load_config():
    """Load configuration"""
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def load_model(model_path):
    """Load trained model"""
    with open(model_path, "rb") as f:
        return pickle.load(f)

def load_test_data(data_dir):
    """Load test data"""
    X_test = pd.read_csv(Path(data_dir) / "X_test.csv")
    y_test = pd.read_csv(Path(data_dir) / "y_test.csv").values.ravel()
    return X_test, y_test

def evaluate_model(model, X_test, y_test):
    """Evaluate model on test set"""
    y_pred = model.predict(X_test)
    
    metrics = {
        "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
        "mae": float(mean_absolute_error(y_test, y_pred)),
        "r2": float(r2_score(y_test, y_pred)),
        "mape": float(np.mean(np.abs((y_test - y_pred) / y_test)) * 100)
    }
    
    return metrics, y_pred

def create_visualizations(y_test, y_pred, output_dir):
    """Create evaluation plots"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Actual vs Predicted
    plt.figure(figsize=(10, 6))
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
    plt.xlabel('Actual Charges')
    plt.ylabel('Predicted Charges')
    plt.title('Actual vs Predicted Insurance Charges')
    plt.tight_layout()
    plt.savefig(output_path / "actual_vs_predicted.png")
    plt.close()
    
    # Residuals plot
    residuals = y_test - y_pred
    plt.figure(figsize=(10, 6))
    plt.scatter(y_pred, residuals, alpha=0.5)
    plt.axhline(y=0, color='r', linestyle='--')
    plt.xlabel('Predicted Charges')
    plt.ylabel('Residuals')
    plt.title('Residuals Plot')
    plt.tight_layout()
    plt.savefig(output_path / "residuals.png")
    plt.close()
    
    # Distribution of errors
    plt.figure(figsize=(10, 6))
    plt.hist(residuals, bins=50, edgecolor='black')
    plt.xlabel('Residuals')
    plt.ylabel('Frequency')
    plt.title('Distribution of Prediction Errors')
    plt.tight_layout()
    plt.savefig(output_path / "error_distribution.png")
    plt.close()
    
    print(f"Visualizations saved to {output_dir}")

def main():
    """Main evaluation pipeline"""
    config = load_config()
    
    # Load model and data
    model = load_model("models/model.pkl")
    X_test, y_test = load_test_data(config['data']['processed_dir'])
    
    # Evaluate
    metrics, y_pred = evaluate_model(model, X_test, y_test)
    
    print("\nModel Evaluation Metrics:")
    for metric_name, value in metrics.items():
        print(f"  {metric_name.upper()}: {value:.4f}")
    
    # Save metrics
    metrics_dir = Path("metrics")
    metrics_dir.mkdir(exist_ok=True)
    
    with open(metrics_dir / "evaluation.json", "w") as f:
        json.dump(metrics, f, indent=2)
    
    # Create visualizations
    create_visualizations(y_test, y_pred, "metrics/plots")
    
    print("\n✓ Evaluation completed!")

if __name__ == "__main__":
    main()