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
    features = metadata["features"]
    print("Model loaded successfully!")
except Exception as e:
    print("Model load failed:", e)
    features = []

# ---- Routes ---- #
@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        data = request.json
        values = [data.get(f, 0) for f in features]

        prediction = model.predict([values])[0]
        return jsonify({
            "status": "success",
            "predicted_range_km": float(prediction)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_msg = data.get("message", "").lower()

    # Extract EV features (key:value) even inside sentences
    feature_map = {}
    for word in user_msg.replace(",", " ").split():
        if ":" in word:
            k, v = word.split(":")
            feature_map[k] = v

    # If the user gives any EV specs → predict immediately
    if feature_map:
        missing = [f for f in required_features if f not in feature_map]
        if missing:
            return jsonify({
                "reply": f"Missing features: {missing}\n"
                         f"Provide values like: torque_nm:450 efficiency_wh_per_km:180"
            })

        try:
            x = [[float(feature_map[f]) for f in required_features]]
            pred = model.predict(x)[0]
            return jsonify({
                "reply": f"⚡ Estimated EV range: {pred:.2f} km"
            })

        except:
            return jsonify({"reply": "Some values are invalid. Please check format!"})

    # Normal conversation fallback
    response = f"Send EV specs like:\n" \
               f"battery_capacity_kWh:75 torque_nm:450 efficiency_wh_per_km:180"
    return jsonify({"reply": response})



@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "EV Range Predictor API Running"})


if __name__ == "__main__":
    app.run(debug=True)
