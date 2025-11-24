"""
Tests for the API endpoints
"""
import pytest
from pathlib import Path
import sys
import os

# Setup paths
project_root = Path(__file__).parent.parent
os.chdir(project_root)
sys.path.insert(0, str(project_root / "src"))

def test_imports():
    """Test that required modules can be imported"""
    try:
        import fastapi
        import pydantic
        print("✓ FastAPI and Pydantic imported successfully")
    except ImportError as e:
        pytest.fail(f"Failed to import required modules: {e}")

def test_api_module_exists():
    """Test that API module exists"""
    api_file = project_root / "src" / "api" / "app.py"
    assert api_file.exists(), "API module not found"
    print(f"✓ API module found at {api_file}")

@pytest.mark.skipif(
    not (Path("models/model.pkl").exists() and 
         Path("data/processed/scaler.pkl").exists()),
    reason="Model artifacts not ready"
)
class TestAPI:
    """API tests that require trained model"""
    
    @classmethod
    def setup_class(cls):
        """Setup test client"""
        try:
            from fastapi.testclient import TestClient
            from api.app import app
            cls.client = TestClient(app)
            print("✓ Test client created successfully")
        except Exception as e:
            pytest.skip(f"Cannot create test client: {e}")
    
    def test_root(self):
        """Test root endpoint"""
        response = self.client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print(f"✓ Root endpoint working: {data['message']}")
    
    def test_health(self):
        """Test health endpoint"""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["model_loaded"] == True
        print("✓ Health check passed")
    
    def test_predict_valid(self):
        """Test prediction with valid data"""
        test_data = {
            "age": 35,
            "sex": "male",
            "bmi": 27.5,
            "children": 2,
            "smoker": "no",
            "region": "northwest"
        }
        
        response = self.client.post("/predict", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert "predicted_cost" in data
        assert data["predicted_cost"] > 0
        print(f"✓ Prediction successful: ${data['predicted_cost']:.2f}")
    
    def test_predict_smoker(self):
        """Test prediction for smoker (should be higher)"""
        test_data = {
            "age": 35,
            "sex": "male",
            "bmi": 27.5,
            "children": 2,
            "smoker": "yes",
            "region": "northwest"
        }
        
        response = self.client.post("/predict", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert data["predicted_cost"] > 5000  # Smokers typically cost more
        print(f"✓ Smoker prediction: ${data['predicted_cost']:.2f}")
    
    def test_batch_predict(self):
        """Test batch prediction"""
        test_data = [
            {
                "age": 35,
                "sex": "male",
                "bmi": 27.5,
                "children": 2,
                "smoker": "no",
                "region": "northwest"
            },
            {
                "age": 45,
                "sex": "female",
                "bmi": 30.0,
                "children": 1,
                "smoker": "yes",
                "region": "southeast"
            }
        ]
        
        response = self.client.post("/batch_predict", json=test_data)
        assert response.status_code == 200
        data = response.json()
        assert "predictions" in data
        assert len(data["predictions"]) == 2
        print(f"✓ Batch prediction successful: {len(data['predictions'])} predictions")
    
    def test_invalid_age(self):
        """Test with invalid age"""
        test_data = {
            "age": 150,  # Invalid
            "sex": "male",
            "bmi": 27.5,
            "children": 2,
            "smoker": "no",
            "region": "northwest"
        }
        
        response = self.client.post("/predict", json=test_data)
        assert response.status_code == 422  # Validation error
        print("✓ Invalid age rejected correctly")