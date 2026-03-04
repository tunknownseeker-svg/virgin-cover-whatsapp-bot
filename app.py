from flask import Flask, request, jsonify

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
        if verify_token == "mytoken123":
            return challenge
        return "Invalid verification token"
    else:
        return jsonify(status="ok")

if __name__ == "__main__":
    app.run(port=5000)