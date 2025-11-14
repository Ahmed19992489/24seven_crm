from flask import Flask, request
import requests

app = Flask(__name__)

# توكنات الفيسبوك
VERIFY_TOKEN = "hamouksha_token"      # ده ثابت للتحقق
PAGE_TOKEN = "EAALF8MeR7twBP9sLZBBzNmbTuPAnPZBZCYqpoc7gpftDYKqScrENxSNiQgm9fpcEJaGlyNZASqUpydNBWNi5d8XaskgZC73BX0WhnQR1dQS7Xl7bvfmWdzLBXn3tmJC1wbyzv8D28j5Tjo5daApXlfIXVJT8OumnKQChMVaE3JHP9oZBblSMFPAd4aUwJVtNfcRgZAaPC6mTNLJAZCGgU2QMlnQZD"


# ------------------------------------------------------------------
#   1) التحقق من Webhook
# ------------------------------------------------------------------
@app.route("/", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200

    return "Verification failed", 403


# ------------------------------------------------------------------
#   2) استقبال الرسالة من المستخدم
# ------------------------------------------------------------------
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    try:
        messaging = data["entry"][0]["messaging"][0]

        sender_id = messaging["sender"]["id"]
        message_text = messaging["message"].get("text", "")

        # الرد
        reply = (
            "👋 أهلاً بيك في **24seven Bot**\n"
            f"إنت كتبت: {message_text}\n"
            "لو محتاج تحجز عربية أو تستفسر عن الأسعار — أنا جاهز معاك 🚗🔥"
        )

        send_message(sender_id, reply)

    except Exception as e:
        print("Error:", e)

    return "ok", 200


# ------------------------------------------------------------------
#   3) إرسال الرسالة للعميل
# ------------------------------------------------------------------
def send_message(recipient_id, text):
    url = f"https://graph.facebook.com/v19.0/me/messages?access_token={PAGE_TOKEN}"

    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text}
    }

    response = requests.post(url, json=payload)
    print("Send message status:", response.status_code, response.text)


# ------------------------------------------------------------------
#   4) تشغيل السيرفر
# ------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
