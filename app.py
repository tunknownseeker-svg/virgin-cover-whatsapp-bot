from flask import Flask, request, jsonify
import os

app = Flask(__name__)

@app.route("/")
def home():
    return "Virgin Cover Bot is running"

@app.route("/whatsapp", methods=["GET","POST"])
def whatsapp():
    if request.method == "GET":
        verify_token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")
        if verify_token == "mytoken123":  # replace with your chosen token
            return challenge
        return "Invalid verification token"
    else:
        return jsonify(status="ok")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, threaded=True)