from flask import Flask, request, jsonify, send_from_directory
import joblib
import os

app = Flask(__name__)

# Load model
MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "models", "model_clean.joblib")
model = joblib.load(MODEL_PATH)


@app.route("/")
def home():
    """Serve frontend UI"""
    static_path = os.path.join(os.path.dirname(__file__), "..", "static")
    return send_from_directory(static_path, "chat_ui.html")


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()

    if "features" not in data:
        return jsonify({"error": "Missing 'features'"}), 400

    features = data["features"]

    try:
        prediction = model.predict([features])[0]
        return jsonify({"range_prediction": float(prediction)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/chat", methods=["POST"])
def chat():
    """Your existing chat_openai logic here"""
    from backend.chat_openai import generate_reply
    message = request.json.get("message", "")
    response = generate_reply(message)
    return jsonify({"reply": response})


@app.route("/static/<path:path>")
def serve_static(path):
    static_path = os.path.join(os.path.dirname(__file__), "..", "static")
    return send_from_directory(static_path, path)


# Needed for Vercel
handler = app
