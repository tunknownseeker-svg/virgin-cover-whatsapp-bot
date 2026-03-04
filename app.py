from flask import Flask, request, jsonify
import os  # Needed for Render port

app = Flask(__name__)

@app.route("/")
def home():
    return "Virgin Cover Bot is running"

@app.route("/whatsapp", methods=["GET","POST"])
def whatsapp():
    if request.method == "GET":
        # Verification token for Meta webhook
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if verify_token == "mytoken123":  # <-- Replace with your chosen token
            return challenge
        return "Invalid verification token"
    else:
        return jsonify(status="ok")

# Updated for Render deployment
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render's assigned port or default 5000 locally
    app.run(host="0.0.0.0", port=port, threaded=True)