import os
import uuid
import json
import joblib
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from openai import OpenAI

# -------------------------
# Load API key
# -------------------------
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -------------------------
# Flask App
# -------------------------
app = Flask(__name__, static_folder="../static")
CORS(app)

# -------------------------
# Model + Metadata
# -------------------------
import os.path
model_path = os.path.join(os.path.dirname(__file__), "../Models/model_clean.joblib")
metadata_path = os.path.join(os.path.dirname(__file__), "../Models/metadata.json")
model = joblib.load(model_path)
metadata = json.load(open(metadata_path))
REQUIRED = metadata["features"]

SESSIONS = {}

# --------------------------------------------------
# Serve Frontend UI
# --------------------------------------------------
@app.route("/")
def frontend():
    return send_from_directory("../static", "chat_ui.html")


# --------------------------------------------------
# Start Chat Session
# --------------------------------------------------
@app.route("/chat/start", methods=["POST"])
def start_chat():
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = {"data": {}}
    return jsonify({"session_id": session_id})


# --------------------------------------------------
# Chat Endpoint
# --------------------------------------------------
@app.route("/chat/<session_id>", methods=["POST"])
def chat(session_id):

    if session_id not in SESSIONS:
        return jsonify({"error": "session_not_found"}), 404

    data = SESSIONS[session_id]["data"]
    msg = request.json.get("message", "")

    # 1. Parse key:value inputs
    added = {}
    for p in msg.split():
        if ":" in p:
            k, v = p.split(":")
            try:
                data[k] = float(v)
                added[k] = float(v)
            except:
                pass

    if added:
        return jsonify({"reply": f"Saved: Type 'predict' when ready."})

    # 2. Prediction
    if "predict" in msg.lower():
        missing = [f for f in REQUIRED if f not in data]
        if missing:
            return jsonify({"reply": f"Missing features: {missing}"})

        x = [[data[f] for f in REQUIRED]]
        pred = model.predict(x)[0]

        return jsonify({"reply": f"Estimated range: {pred:.2f} km"})

    # 3. Default response
    return jsonify({"reply": "Send EV features like: battery_capacity_kWh:75"})


# --------------------------------------------------
# Run Server
# --------------------------------------------------
if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
