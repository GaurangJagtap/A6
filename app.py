import os
import joblib
import numpy as np
from flask import Flask, request, jsonify

app = Flask(__name__)

# Class labels for Iris dataset
CLASS_NAMES = ["setosa", "versicolor", "virginica"]

# Resolve model path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.joblib")

# Load trained model
model = None
if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        print(f"[INFO] Model loaded successfully from {MODEL_PATH}")
    except Exception as e:
        print(f"[ERROR] Failed to load model from {MODEL_PATH}: {e}")
else:
    print(f"[WARNING] Model file not found at {MODEL_PATH}. Run train_model.py first.")


@app.route("/", methods=["GET"])
def home():
    """Root endpoint to check API status."""
    return jsonify({"message": "Iris Model API is running"}), 200


@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "model_loaded": model is not None,
        "classes": CLASS_NAMES
    }), 200


@app.route("/predict", methods=["POST"])
def predict():
    """Prediction endpoint expecting JSON: {"features": [f1, f2, f3, f4]}."""
    global model

    if model is None:
        # Attempt to reload model if it wasn't available at startup
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
        else:
            return jsonify({
                "error": "Model is not loaded. Ensure model.joblib exists in the project root."
            }), 500

    # 1. Validate JSON payload
    if not request.is_json:
        return jsonify({
            "error": "Invalid Content-Type. Request must be application/json with a valid JSON body."
        }), 400

    data = request.get_json(silent=True)
    if data is None:
        return jsonify({
            "error": "Malformed JSON payload. Please provide valid JSON."
        }), 400

    # 2. Validate 'features' key presence
    if "features" not in data:
        return jsonify({
            "error": "Missing 'features' field in JSON request. Expected: {'features': [f1, f2, f3, f4]}"
        }), 400

    features = data["features"]

    # 3. Validate features type
    if not isinstance(features, list):
        return jsonify({
            "error": "'features' must be a JSON array/list of numbers."
        }), 400

    # 4. Validate exact length of 4 features
    if len(features) != 4:
        return jsonify({
            "error": f"Invalid feature length: Expected exactly 4 numerical features (sepal_length, sepal_width, petal_length, petal_width), but received {len(features)}."
        }), 400

    # 5. Validate that all values are valid numbers (not boolean, not string, not None, not infinite or NaN)
    parsed_features = []
    for idx, val in enumerate(features):
        if isinstance(val, bool) or not isinstance(val, (int, float)):
            return jsonify({
                "error": f"Invalid feature value at index {idx}: '{val}'. All features must be numeric (int or float)."
            }), 400
        if np.isnan(val) or np.isinf(val):
            return jsonify({
                "error": f"Feature at index {idx} contains NaN or Infinity, which is not permitted."
            }), 400
        parsed_features.append(float(val))

    # 6. Predict using model
    try:
        input_data = np.array(parsed_features, dtype=float).reshape(1, -1)
        pred_idx = int(model.predict(input_data)[0])
        predicted_flower = CLASS_NAMES[pred_idx]
        return jsonify({
            "prediction": predicted_flower
        }), 200
    except Exception as e:
        return jsonify({
            "error": f"Inference error during model prediction: {str(e)}"
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

