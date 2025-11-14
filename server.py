from flask import Flask, request
import os

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")


@app.route("/", methods=["GET"])
def home():
    return "24Seven CRM Bot is running!", 200


# ---------------------------------------------
#   WEBHOOK VERIFICATION (REQUIRED BY META)
# ---------------------------------------------
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    else:
        return "Verification token mismatch", 403


# ---------------------------------------------
#   WEBHOOK MESSAGES (POST)
# ---------------------------------------------
@app.route("/webhook", methods=["POST"])
def messages():
    data = request.get_json()

    print("📩 Received message:", data)

    return "EVENT_RECEIVED", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
