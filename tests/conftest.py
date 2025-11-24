"""
Pytest configuration and fixtures
"""
import pytest
import sys
import os
from pathlib import Path

# Get project root
project_root = Path(__file__).parent.parent
os.chdir(project_root)

# Add to Python path
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

print(f"Project root: {project_root}")
print(f"Python path: {sys.path[:3]}")

@pytest.fixture(scope="session")
def project_root_dir():
    """Return project root directory"""
    return project_root

@pytest.fixture(scope="session")
def model_ready(project_root_dir):
    """Check if model and preprocessing artifacts are ready"""
    model_file = project_root_dir / "models" / "model.pkl"
    scaler_file = project_root_dir / "data" / "processed" / "scaler.pkl"
    encoders_file = project_root_dir / "data" / "processed" / "label_encoders.pkl"
    
    all_ready = all([
        model_file.exists(),
        scaler_file.exists(),
        encoders_file.exists()
    ])
    
    if not all_ready:
        pytest.skip("Model artifacts not ready. Run training pipeline first.")
    
    return all_ready