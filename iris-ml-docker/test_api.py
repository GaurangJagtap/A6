import json
import requests
import sys

BASE_URL = "http://localhost:5000"


def test_endpoints():
    print("=" * 65)
    print("RUNNING API TEST SUITE (Iris ML Model API)")
    print("=" * 65)

    # 1. Test Root Endpoint
    print("\n[TEST 1] GET / (Root Endpoint)")
    try:
        res = requests.get(f"{BASE_URL}/")
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.json()}")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        assert res.json().get("message") == "Iris Model API is running"
        print(">>> PASS: Root endpoint verified.")
    except Exception as e:
        print(f">>> FAIL: {e}")
        return False

    # 2. Test Health Endpoint
    print("\n[TEST 2] GET /health (Health Check Endpoint)")
    try:
        res = requests.get(f"{BASE_URL}/health")
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.json()}")
        assert res.status_code == 200, f"Expected 200, got {res.status_code}"
        assert res.json().get("status") == "healthy"
        print(">>> PASS: Health endpoint verified.")
    except Exception as e:
        print(f">>> FAIL: {e}")
        return False

    # 3. Test Prediction 1 (Setosa)
    print("\n[TEST 3] POST /predict (Sample 1: Setosa)")
    payload_setosa = {"features": [5.1, 3.5, 1.4, 0.2]}
    try:
        res = requests.post(
            f"{BASE_URL}/predict",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload_setosa)
        )
        print(f"Input: {payload_setosa}")
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.json()}")
        assert res.status_code == 200
        assert res.json().get("prediction") == "setosa"
        print(">>> PASS: Correctly predicted 'setosa'.")
    except Exception as e:
        print(f">>> FAIL: {e}")
        return False

    # 4. Test Prediction 2 (Versicolor)
    print("\n[TEST 4] POST /predict (Sample 2: Versicolor)")
    payload_versicolor = {"features": [6.0, 2.7, 5.1, 1.6]}
    try:
        res = requests.post(
            f"{BASE_URL}/predict",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload_versicolor)
        )
        print(f"Input: {payload_versicolor}")
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.json()}")
        assert res.status_code == 200
        assert res.json().get("prediction") == "versicolor"
        print(">>> PASS: Correctly predicted 'versicolor'.")
    except Exception as e:
        print(f">>> FAIL: {e}")
        return False

    # 5. Test Prediction 3 (Virginica)
    print("\n[TEST 5] POST /predict (Sample 3: Virginica)")
    payload_virginica = {"features": [6.7, 3.3, 5.7, 2.5]}
    try:
        res = requests.post(
            f"{BASE_URL}/predict",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload_virginica)
        )
        print(f"Input: {payload_virginica}")
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.json()}")
        assert res.status_code == 200
        assert res.json().get("prediction") == "virginica"
        print(">>> PASS: Correctly predicted 'virginica'.")
    except Exception as e:
        print(f">>> FAIL: {e}")
        return False

    # 6. Test Invalid Input: Wrong feature count
    print("\n[TEST 6] POST /predict (Invalid Input: 2 features instead of 4)")
    payload_invalid_len = {"features": [5.1, 3.5]}
    try:
        res = requests.post(
            f"{BASE_URL}/predict",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload_invalid_len)
        )
        print(f"Input: {payload_invalid_len}")
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.json()}")
        assert res.status_code == 400
        assert "error" in res.json()
        print(">>> PASS: Correctly rejected invalid feature count with 400.")
    except Exception as e:
        print(f">>> FAIL: {e}")
        return False

    # 7. Test Invalid Input: Non-numeric value
    print("\n[TEST 7] POST /predict (Invalid Input: string in features)")
    payload_invalid_type = {"features": [5.1, "invalid_num", 1.4, 0.2]}
    try:
        res = requests.post(
            f"{BASE_URL}/predict",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload_invalid_type)
        )
        print(f"Input: {payload_invalid_type}")
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.json()}")
        assert res.status_code == 400
        assert "error" in res.json()
        print(">>> PASS: Correctly rejected non-numeric feature with 400.")
    except Exception as e:
        print(f">>> FAIL: {e}")
        return False

    # 8. Test Invalid Input: Missing features key
    print("\n[TEST 8] POST /predict (Invalid Input: missing 'features' key)")
    payload_missing_key = {"wrong_key": [1, 2, 3, 4]}
    try:
        res = requests.post(
            f"{BASE_URL}/predict",
            headers={"Content-Type": "application/json"},
            data=json.dumps(payload_missing_key)
        )
        print(f"Input: {payload_missing_key}")
        print(f"Status Code: {res.status_code}")
        print(f"Response: {res.json()}")
        assert res.status_code == 400
        assert "error" in res.json()
        print(">>> PASS: Correctly rejected missing features key with 400.")
    except Exception as e:
        print(f">>> FAIL: {e}")
        return False

    print("\n" + "=" * 65)
    print("ALL 8 API TESTS PASSED SUCCESSFULLY!")
    print("=" * 65)
    return True


if __name__ == "__main__":
    success = test_endpoints()
    sys.exit(0 if success else 1)

