from flask import Flask, request, jsonify
from flask_cors import CORS
import os


from utils.summarizer import summarize_email
from utils.auto_reply import generate_reply
from utils.prediction import predict_email, predict_long_email


app = Flask(__name__)


CORS(app)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "running",
        "message": "Smart Email AI API is live 🚀"
    })



@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json() or {}
        email = data.get("email", "")

        if not email.strip():
            return jsonify({"error": "Email is required"}), 400

        result = predict_email(email)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/predict-long", methods=["POST"])
def predict_long():
    try:
        data = request.get_json() or {}
        email = data.get("email", "")

        if not email.strip():
            return jsonify({"error": "Email is required"}), 400

        result = predict_long_email(email)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/summarize", methods=["POST"])
def summarize():
    try:
        print("REQUEST HIT /summarize")
        print(request.get_json())
        data = request.get_json() or {}
        email = data.get("email", "")

        if not email.strip():
            return jsonify({"error": "Email is required"}), 400

        summary = summarize_email(email)

        return jsonify({
            "summary": summary
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app.route("/auto-reply", methods=["POST"])
def auto_reply():
    
    try:
        print("REQUEST HIT /autoreply")
        print(request.get_json())
        data = request.get_json() or {}

        email = data.get("email", "")
        tone = data.get("tone", "professional")
        print("Selected tone:", tone)

        if not email.strip():
            return jsonify({"error": "Email is required"}), 400

        reply = generate_reply(email, tone)

        return jsonify({
            "reply": reply,
            "tone": tone
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )