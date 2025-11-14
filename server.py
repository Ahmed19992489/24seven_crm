from flask import Flask, request, jsonify
import requests
import json  # مهم علشان نطبع الداتا

app = Flask(__name__)

# ⚠️ خلى بالك: حط الـ PAGE_ACCESS_TOKEN بتاعك هنا
PAGE_ACCESS_TOKEN = "EAALF8MeR7twBP9sLZBBzNmbTuPAnPZBZCYqpoc7gpftDYKqScrENxSNiQgm9fpcEJaGlyNZASqUpydNBWNi5d8XaskgZC73BX0WhnQR1dQS7Xl7bvfmWdzLBXn3tmJC1wbyzv8D28j5Tjo5daApXlfIXVJT8OumnKQChMVaE3JHP9oZBblSMFPAd4aUwJVtNfcRgZAaPC6mTNLJAZCGgU2QMlnQZDا"

VERIFY_TOKEN = "24seven_token"  # نفس اللى فى شاشة Messenger API Settings

def send_message(recipient_id, message_text):
    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, json=payload, headers=headers)
    print("📤 Facebook response:", response.status_code, response.text)


# ✅ خطوة التحقق من الـ webhook
@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    print("🔎 VERIFY CALL:", mode, token, challenge)

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Webhook verified successfully")
        return challenge, 200
    else:
        print("❌ Webhook verification failed")
        return "Error validating token", 403


# ✅ استقبال الرسائل من فيسبوك
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    print("📩 Incoming webhook:")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for event in entry.get("messaging", []):
                sender_id = event["sender"]["id"]

                if "message" in event and "text" in event["message"]:
                    user_message = event["message"]["text"]
                    print(f"👤 User ({sender_id}) said: {user_message}")

                    bot_reply = f"استقبلت رسالتك: {user_message}"
                    send_message(sender_id, bot_reply)

        return "EVENT_RECEIVED", 200

    return "ERROR", 404


if __name__ == "__main__":
    app.run(port=5000, debug=True)
