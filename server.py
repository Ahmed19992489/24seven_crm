from flask import Flask, request
import os
import requests

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("24seven_token")
PAGE_ACCESS_TOKEN = os.getenv("EAALF8MeR7twBP9sLZBBzNmbTuPAnPZBZCYqpoc7gpftDYKqScrENxSNiQgm9fpcEJaGlyNZASqUpydNBWNi5d8XaskgZC73BX0WhnQR1dQS7Xl7bvfmWdzLBXn3tmJC1wbyzv8D28j5Tjo5daApXlfIXVJT8OumnKQChMVaE3JHP9oZBblSMFPAd4aUwJVtNfcRgZAaPC6mTNLJAZCGgU2QMlnQZD")


@app.route("/", methods=["GET"])
def home():
    return "24Seven CRM Bot is running!", 200


# ---------------------------------------------
#   WEBHOOK VERIFICATION (GET)
# ---------------------------------------------
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("✅ Webhook verified successfully")
        return challenge, 200
    else:
        print("❌ Webhook verification failed")
        return "Verification token mismatch", 403


# ---------------------------------------------
#   HANDLE INCOMING MESSAGES (POST)
# ---------------------------------------------
@app.route("/webhook", methods=["POST"])
def handle_messages():
    data = request.get_json()
    print("📩 Received payload:", data)

    # تأكد إن الحدث جاي من Page
    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for messaging_event in entry.get("messaging", []):
                sender_id = messaging_event.get("sender", {}).get("id")
                message = messaging_event.get("message")

                # لو في رسالة نصية من العميل
                if sender_id and message and "text" in message:
                    user_text = message["text"]
                    print(f"💬 From {sender_id}: {user_text}")

                    # رد بسيط كبداية (Echo + ترحيب)
                    reply_text = (
                        "👋 أهلاً بيك في 24Seven Limousine!\n"
                        f"انت كتبت: {user_text}\n\n"
                        "إبعتلي:\n"
                        "- اسمك\n"
                        "- نقطة الانطلاق\n"
                        "- نقطة الوصول\n"
                        "- ميعاد الرحلة\n"
                        "عشان أساعدك في الحجز 💚"
                    )

                    send_message(sender_id, reply_text)

    return "EVENT_RECEIVED", 200


# ---------------------------------------------
#   SEND MESSAGE TO USER VIA MESSENGER
# ---------------------------------------------
def send_message(recipient_id, text):
    url = "https://graph.facebook.com/v21.0/me/messages"
    params = {"access_token": PAGE_ACCESS_TOKEN}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }

    try:
        r = requests.post(url, params=params, json=payload)
        print("📤 Send API response:", r.status_code, r.text)
    except Exception as e:
        print("❌ Error sending message:", e)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # في التطوير المحلي بس
    app.run(host="0.0.0.0", port=port)
