"""
Script to test API endpoints
"""
import requests
import json

def check_server_running():
    """Check if API server is running"""
    try:
        response = requests.get("http://localhost:8000/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def print_response(response):
    """Print response with error handling"""
    print(f"   Status: {response.status_code}")
    try:
        data = response.json()
        print(f"   Response: {json.dumps(data, indent=2)}")
        return data
    except:
        print(f"   Response: {response.text}")
        return None

def test_root():
    """Test root endpoint"""
    print("\n1. Testing root endpoint...")
    try:
        response = requests.get("http://localhost:8000/")
        data = print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_health():
    """Test health endpoint"""
    print("\n2. Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8000/health")
        data = print_response(response)
        return response.status_code == 200 and data.get('model_loaded', False)
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_model_info():
    """Test model info endpoint"""
    print("\n3. Testing model info endpoint...")
    try:
        response = requests.get("http://localhost:8000/model-info")
        data = print_response(response)
        return response.status_code == 200
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_prediction():
    """Test prediction endpoint"""
    print("\n4. Testing prediction endpoint (non-smoker)...")
    
    test_data = {
        "age": 35,
        "sex": "male",
        "bmi": 27.5,
        "children": 2,
        "smoker": "no",
        "region": "northwest"
    }
    
    print(f"   Input: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json=test_data
        )
        data = print_response(response)
        
        if response.status_code == 200 and data:
            print(f"   ✓ Predicted Cost: ${data['predicted_cost']:.2f}")
            return True
        else:
            print(f"   ❌ Prediction failed")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_smoker_prediction():
    """Test prediction for smoker"""
    print("\n5. Testing smoker prediction...")
    
    test_data = {
        "age": 35,
        "sex": "male",
        "bmi": 27.5,
        "children": 2,
        "smoker": "yes",
        "region": "northwest"
    }
    
    print(f"   Input: {json.dumps(test_data, indent=2)}")
    
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json=test_data
        )
        data = print_response(response)
        
        if response.status_code == 200 and data:
            print(f"   ✓ Predicted Cost: ${data['predicted_cost']:.2f}")
            print(f"   Note: Smokers typically have higher costs")
            return True
        else:
            print(f"   ❌ Prediction failed")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_batch_prediction():
    """Test batch prediction"""
    print("\n6. Testing batch prediction...")
    
    test_data = [
        {
            "age": 25,
            "sex": "female",
            "bmi": 22.5,
            "children": 0,
            "smoker": "no",
            "region": "northeast"
        },
        {
            "age": 45,
            "sex": "male",
            "bmi": 30.0,
            "children": 2,
            "smoker": "yes",
            "region": "southeast"
        },
        {
            "age": 55,
            "sex": "female",
            "bmi": 28.0,
            "children": 1,
            "smoker": "no",
            "region": "southwest"
        }
    ]
    
    try:
        response = requests.post(
            "http://localhost:8000/batch_predict",
            json=test_data
        )
        data = print_response(response)
        
        if response.status_code == 200 and data:
            print(f"   ✓ Number of predictions: {data['count']}")
            for i, cost in enumerate(data['predictions'], 1):
                if cost is not None:
                    print(f"   Patient {i}: ${cost:.2f}")
                else:
                    print(f"   Patient {i}: Error")
            return True
        else:
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def test_invalid_input():
    """Test with invalid input"""
    print("\n7. Testing invalid input (should fail gracefully)...")
    
    test_data = {
        "age": 35,
        "sex": "invalid",  # Invalid value
        "bmi": 27.5,
        "children": 2,
        "smoker": "no",
        "region": "northwest"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/predict",
            json=test_data
        )
        data = print_response(response)
        
        if response.status_code == 400:
            print(f"   ✓ Invalid input correctly rejected")
            return True
        else:
            print(f"   ⚠️  Expected error but got status {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def main():
    """Main test function"""
    print("="*70)
    print("API ENDPOINT TESTING")
    print("="*70)
    
    # Check if server is running
    print("\nChecking if API server is running...")
    if not check_server_running():
        print("\n❌ API server is not running!")
        print("\nPlease start the server first:")
        print("  1. Open a new terminal")
        print("  2. Run: python start_api.py")
        print("  3. Wait for server to start")
        print("  4. Run this script again")
        return False
    
    print("✓ API server is running")
    
    # Run tests
    results = []
    results.append(("Root Endpoint", test_root()))
    results.append(("Health Check", test_health()))
    results.append(("Model Info", test_model_info()))
    results.append(("Single Prediction (Non-smoker)", test_prediction()))
    results.append(("Single Prediction (Smoker)", test_smoker_prediction()))
    results.append(("Batch Prediction", test_batch_prediction()))
    results.append(("Invalid Input Handling", test_invalid_input()))
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "❌ FAIL"
        print(f"{status} - {name}")
    
    total = len(results)
    passed = sum(1 for _, p in results if p)
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("="*70)
    
    return passed == total

if __name__ == "__main__":
    import sys
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTests interrupted")
        sys.exit(1)