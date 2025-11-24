"""
FastAPI application for insurance cost prediction
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict
import pickle
import pandas as pd
import numpy as np
from pathlib import Path
import yaml
import traceback

# Initialize FastAPI app
app = FastAPI(
    title="Medical Insurance Cost Prediction API",
    description="API for predicting medical insurance costs based on patient information",
    version="1.0.0"
)

# Global variables for model and preprocessors
model = None
scaler = None
label_encoders = None
config = None

class InsuranceFeatures(BaseModel):
    """Input features for insurance cost prediction"""
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "age": 35,
                "sex": "male",
                "bmi": 27.5,
                "children": 2,
                "smoker": "no",
                "region": "northwest"
            }
        }
    )
    
    age: int = Field(..., ge=18, le=100, description="Age of the person")
    sex: str = Field(..., description="Gender (male/female)")
    bmi: float = Field(..., ge=10, le=60, description="Body Mass Index")
    children: int = Field(..., ge=0, le=10, description="Number of children")
    smoker: str = Field(..., description="Smoking status (yes/no)")
    region: str = Field(..., description="Residential region (northeast/northwest/southeast/southwest)")

class PredictionResponse(BaseModel):
    """Response model for predictions"""
    model_config = ConfigDict(protected_namespaces=())
    
    predicted_cost: float
    model_version: str

def load_artifacts():
    """Load model and preprocessing artifacts"""
    global model, scaler, label_encoders, config
    
    try:
        # Load config
        with open("config.yaml", "r") as f:
            config = yaml.safe_load(f)
        
        # Load model
        with open("models/model.pkl", "rb") as f:
            model = pickle.load(f)
        
        # Load preprocessors
        processed_dir = Path(config['data']['processed_dir'])
        with open(processed_dir / "scaler.pkl", "rb") as f:
            scaler = pickle.load(f)
        
        with open(processed_dir / "label_encoders.pkl", "rb") as f:
            label_encoders = pickle.load(f)
        
        print("✓ All artifacts loaded successfully")
        print(f"✓ Label encoders available for: {list(label_encoders.keys())}")
        
    except Exception as e:
        print(f"Error loading artifacts: {e}")
        traceback.print_exc()
        raise

@app.on_event("startup")
async def startup_event():
    """Load model on startup"""
    load_artifacts()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Medical Insurance Cost Prediction API",
        "version": "1.0.0",
        "endpoints": {
            "predict": "/predict",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "encoders_loaded": label_encoders is not None
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict(features: InsuranceFeatures):
    """Predict insurance cost"""
    try:
        # Validate categorical values
        valid_sex = ['male', 'female']
        valid_smoker = ['yes', 'no']
        valid_region = ['northeast', 'northwest', 'southeast', 'southwest']
        
        if features.sex not in valid_sex:
            raise HTTPException(
                status_code=400, 
                detail=f"Invalid sex value. Must be one of: {valid_sex}"
            )
        
        if features.smoker not in valid_smoker:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid smoker value. Must be one of: {valid_smoker}"
            )
        
        if features.region not in valid_region:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid region value. Must be one of: {valid_region}"
            )
        
        # Create dataframe from input
        input_dict = {
            'age': features.age,
            'sex': features.sex,
            'bmi': features.bmi,
            'children': features.children,
            'smoker': features.smoker,
            'region': features.region
        }
        
        input_data = pd.DataFrame([input_dict])
        
        # Create a copy for encoding
        input_encoded = input_data.copy()
        
        # Encode categorical variables
        categorical_cols = ['sex', 'smoker', 'region']
        for col in categorical_cols:
            if col in label_encoders:
                try:
                    # Transform the categorical value
                    input_encoded[col] = label_encoders[col].transform(input_data[col])
                except ValueError as e:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid value for {col}: {input_data[col].iloc[0]}. Error: {str(e)}"
                    )
        
        # Get numerical features from config
        numerical_features = config['features']['numerical']
        
        # Scale only numerical features
        input_scaled = input_encoded.copy()
        input_scaled[numerical_features] = scaler.transform(input_encoded[numerical_features])
        
        # Ensure columns are in the correct order
        feature_cols = numerical_features + categorical_cols
        input_final = input_scaled[feature_cols]
        
        # Make prediction
        prediction = model.predict(input_final)[0]
        
        # Ensure prediction is positive
        prediction = max(0, float(prediction))
        
        return PredictionResponse(
            predicted_cost=prediction,
            model_version="1.0.0"
        )
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"Prediction error: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500, 
            detail=f"Prediction error: {str(e)}"
        )

@app.post("/batch_predict")
async def batch_predict(features_list: list[InsuranceFeatures]):
    """Batch prediction endpoint"""
    try:
        predictions = []
        errors = []
        
        for idx, features in enumerate(features_list):
            try:
                result = await predict(features)
                predictions.append(result.predicted_cost)
            except HTTPException as e:
                errors.append({"index": idx, "error": e.detail})
                predictions.append(None)
            except Exception as e:
                errors.append({"index": idx, "error": str(e)})
                predictions.append(None)
        
        response = {
            "predictions": predictions,
            "count": len([p for p in predictions if p is not None])
        }
        
        if errors:
            response["errors"] = errors
        
        return response
        
    except Exception as e:
        print(f"Batch prediction error: {e}")
        traceback.print_exc()
        raise HTTPException(
            status_code=500, 
            detail=f"Batch prediction error: {str(e)}"
        )

@app.get("/model-info")
async def model_info():
    """Get model information"""
    try:
        return {
            "model_type": type(model).__name__,
            "features": {
                "numerical": config['features']['numerical'],
                "categorical": config['features']['categorical']
            },
            "valid_values": {
                "sex": ["male", "female"],
                "smoker": ["yes", "no"],
                "region": ["northeast", "northwest", "southeast", "southwest"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)