# API Documentation

## Overview

The Medical Insurance Cost Prediction API provides RESTful endpoints for predicting insurance costs based on patient information.

## Base URL

```
http://localhost:8000
```

## Authentication

Currently, the API does not require authentication. For production deployment, consider implementing API key authentication or OAuth2.

## Endpoints

### 1. Root Endpoint

Get basic API information.

**Endpoint:** `GET /`

**Response:**
```json
{
  "message": "Medical Insurance Cost Prediction API",
  "version": "1.0.0",
  "endpoints": {
    "predict": "/predict",
    "health": "/health"
  }
}
```

### 2. Health Check

Check API health status.

**Endpoint:** `GET /health`

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### 3. Single Prediction

Predict insurance cost for a single patient.

**Endpoint:** `POST /predict`

**Request Body:**
```json
{
  "age": 35,
  "sex": "male",
  "bmi": 27.5,
  "children": 2,
  "smoker": "no",
  "region": "northwest"
}
```

**Field Validations:**
- `age`: Integer, 18-100
- `sex`: String, "male" or "female"
- `bmi`: Float, 10-60
- `children`: Integer, 0-10
- `smoker`: String, "yes" or "no"
- `region`: String, "northeast", "northwest", "southeast", or "southwest"

**Response:**
```json
{
  "predicted_cost": 5677.34,
  "model_version": "1.0.0"
}
```

**Status Codes:**
- `200 OK`: Successful prediction
- `422 Unprocessable Entity`: Invalid input data
- `500 Internal Server Error`: Prediction error

### 4. Batch Prediction

Predict insurance costs for multiple patients.

**Endpoint:** `POST /batch_predict`

**Request Body:**
```json
[
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
    "bmi": 32.0,
    "children": 3,
    "smoker": "yes",
    "region": "southeast"
  }
]
```

**Response:**
```json
{
  "predictions": [5677.34, 38764.52],
  "count": 2
}
```

## Error Handling

### Validation Error (422)

```json
{
  "detail": [
    {
      "loc": ["body", "age"],
      "msg": "ensure this value is greater than or equal to 18",
      "type": "value_error.number.not_ge"
    }
  ]
}
```

### Internal Server Error (500)

```json
{
  "detail": "Prediction error: <error message>"
}
```

## Rate Limiting

No rate limiting is currently implemented. For production use, consider implementing rate limiting.

## Interactive Documentation

Access interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc