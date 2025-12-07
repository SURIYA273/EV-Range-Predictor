import os
import json
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ---- Load Model + Metadata ---- #
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../Models/model_clean.joblib")
META_PATH = os.path.join(os.path.dirname(__file__), "../Models/metadata.json")

try:
    model = joblib.load(MODEL_PATH)
    with open(META_PATH, "r") as f:
        metadata = json.load(f)
    feature_order = metadata["feature_order"]
    print("Model loaded successfully!")
except Exception as e:
    print("Model load failed:", e)
    feature_order = []

# ---- Routes ---- #
@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        values = [data.get(f, 0) for f in feature_order]

        prediction = model.predict([values])[0]
        return jsonify({
            "status": "success",
            "predicted_range_km": float(prediction)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "")

        # Basic AI reply (replace later with GPT API)
        bot_response = f"You asked about EVs: {user_message}"

        return jsonify({"reply": bot_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "EV Range Predictor API Running"})


if __name__ == "__main__":
    app.run(debug=True)
