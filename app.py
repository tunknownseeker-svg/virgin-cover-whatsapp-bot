from flask import Flask, request, jsonify
import os

app = Flask(__name__)

VERIFY_TOKEN = "1234567890"  # This must match Meta

@app.route("/")
def home():
    return "Virgin Cover Bot is running"

@app.route("/whatsapp", methods=["GET", "POST"])
def whatsapp():
    if request.method == "GET":
        # Meta sends hub.challenge to verify webhook
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if verify_token == VERIFY_TOKEN and challenge:
            return challenge  # Must return the challenge exactly
        return "Invalid verification token"
    else:
        # Handle incoming messages here
        return jsonify(status="ok")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, threaded=True)