from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

PAGE_ACCESS_TOKEN = "EAALF8MeR7twBP9sLZBBzNmbTuPAnPZBZCYqpoc7gpftDYKqScrENxSNiQgm9fpcEJaGlyNZASqUpydNBWNi5d8XaskgZC73BX0WhnQR1dQS7Xl7bvfmWdzLBXn3tmJC1wbyzv8D28j5Tjo5daApXlfIXVJT8OumnKQChMVaE3JHP9oZBblSMFPAd4aUwJVtNfcRgZAaPC6mTNLJAZCGgU2QMlnQZD"

def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


@app.route("/", methods=["GET"])
def verify():
    verify_token = "24seven_token"
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == verify_token:
        return challenge, 200
    else:
        return "Verification token mismatch", 403


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if data["object"] == "page":
        for entry in data["entry"]:
            for event in entry.get("messaging", []):
                sender_id = event["sender"]["id"]

                if "message" in event and "text" in event["message"]:
                    user_message = event["message"]["text"]

                    # هنا بنرد على الرسالة — عدله زي ما تحب
                    bot_reply = f"استقبلت رسالتك: {user_message}"
                    send_message(sender_id, bot_reply)

        return "EVENT_RECEIVED", 200

    return "ERROR", 404


if __name__ == "__main__":
    app.run(port=5000, debug=True)
