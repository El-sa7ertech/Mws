from flask import Flask , request
import requests
import json
app = Flask(__name__)

VERIFY_TOKEN = "amin"
PAGE_ACCESS_TOKEN = "EAF9Gv1JPuQ8BRCWRq7M2f8RadDzFLEW00kemeOuJBHVEsGQXBIP6cyPgrK9wTFeLhTXtU6SLs7CjdkTQetf1c4wClIvxlzFZCUIhGH0sHSlHkZAY9vgI38smQSxhekgVbvjNIOv5bf4usk6ZBkDYfu2rzelkRh0qNGyZAOPxU6ibtEYev9Jo44d6YkQjT2E1nVKUwSAKTQZDZD"
@app.route("/webhook", methods=["GET"])
def verify_webhook():
    # تحقق عند ربط Webhook مع Facebook
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("Webhook verified!")
        return challenge, 200
    else:
        return "Verification failed", 403
"""
@app.route("/webhook", methods=["POST"])
def handle_messages():
    data = request.get_json()
    print(data)
    if data["object"] == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                sender_id = messaging_event["sender"]["id"]
                message_text = messaging_event.get("message", {}).get("text")
                print(f"Received message from PSID: {sender_id}")
              
                if message_text:
                    print(f"Message text: {message_text}")
    return "EVENT_RECEIVED", 200

if __name__ == "__main__":
    app.run(port=5000, debug=True)"""
@app.route("/webhook", methods=["POST"])
def handle_messages():
    data = request.get_json()
    print(data)
    if data.get("object") == "page":
        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:

                # تأكد أنه رسالة حقيقية
                if "message" in messaging_event:

                    sender_id = messaging_event["sender"]["id"]
                    message_text = messaging_event["message"].get("text")

                    print(f"PSID: {sender_id}")

                    url = f"https://graph.facebook.com/v25.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"

                    payload = {
                        "recipient": {"id": sender_id},
                        "message": {"text": "مرحبا 👋 هذه رسالة من البوت"}
                    }

                    response = requests.post(url, json=payload)
                    print("Send:", response.json())

                    if message_text:
                        print(f"Message text: {message_text}")

    return "EVENT_RECEIVED", 200
if __name__ == "__main__":
    app.run(port=5000, debug=True) 