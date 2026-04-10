import asyncio
import os
from flask import Flask, request
from telethon import TelegramClient, events
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
from threading import Thread
import requests

# ======================
# Facebook Settings
# ======================
VERIFY_TOKEN = "amin"
PAGE_ACCESS_TOKEN = "PUT_YOUR_TOKEN_HERE"

# ======================
# Telegram Settings
# ======================
API_ID = 123456
API_HASH = "your_API_HASH"
bot_username = "mysudan1bot"

tg_loop = asyncio.new_event_loop()
asyncio.set_event_loop(tg_loop)

client = TelegramClient("session", API_ID, API_HASH, loop=tg_loop)

# ======================
# State
# ======================
last_message = None
current_buttons = []
last_psid = None
user_mode = {}
import os
"""
VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
PAGE_ACCESS_TOKEN = os.environ.get("PAGE_ACCESS_TOKEN")
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
bot_username = os.environ.get("BOT_USERNAME")
"""
# ======================
# Facebook Send
# ======================
def send_to_facebook(text):
    if not last_psid:
        return

    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    data = {
        "recipient": {"id": last_psid},
        "message": {"text": text}
    }
    requests.post(url, json=data)

# ======================
# Telegram Events
# ======================
@client.on(events.NewMessage)
@client.on(events.MessageEdited)
async def handler(event):
    global last_message, current_buttons

    sender = await event.get_sender()
    username = sender.username if sender.username else sender.first_name

    if username != bot_username:
        return

    last_message = event.message
    current_buttons = []

    msg = f"📩 Telegram:\n{event.message.text}\n"

    if event.message.buttons:
        buttons_temp = []

        for row in event.message.buttons:
            for btn in row:
                buttons_temp.append(btn)

        buttons_temp.sort(key=lambda b: b.text.lower())
        current_buttons = buttons_temp

        msg += "\n🔘 Buttons:\n"
        for i, btn in enumerate(current_buttons):
            msg += f"{i} - {btn.text}\n"

    send_to_facebook(msg)

# ======================
# Telegram Actions
# ======================
async def send_text(text):
    await client.send_message(bot_username, text)

async def show_last():
    if not last_message:
        send_to_facebook("❌ No message")
        return

    msg = f"📩 Last message:\n{last_message.text}\n"
    send_to_facebook(msg)

async def press_button(index):
    if index >= len(current_buttons):
        send_to_facebook("❌ Invalid button")
        return

    btn = current_buttons[index]

    await client(GetBotCallbackAnswerRequest(
        peer=last_message.to_id,
        msg_id=last_message.id,
        data=btn.data
    ))

    send_to_facebook(f"✅ Pressed: {btn.text}")

# ======================
# Flask App
# ======================
app = Flask(__name__)

@app.route("/webhook", methods=["GET"])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge"), 200
    return "Error", 403


@app.route("/webhook", methods=["POST"])
def webhook():
    global last_psid

    data = request.get_json()
    send_to_facebook(data)
    if data.get("object") == "page":
        for entry in data["entry"]:
            for msg in entry["messaging"]:

                if "message" in msg:
                    sender_id = msg["sender"]["id"]
                    text = msg["message"].get("text")

                    last_psid = sender_id
                    mode = user_mode.get(sender_id)

                    if text == "1":
                        user_mode[sender_id] = "send"
                        send_to_facebook("✏️ Send text")

                    elif text == "2":
                        asyncio.run_coroutine_threadsafe(show_last(), tg_loop)

                    elif mode == "send":
                        asyncio.run_coroutine_threadsafe(send_text(text), tg_loop)
                        send_to_facebook("✅ Sent")

    return "OK", 200

# ======================
# START (FIXED FOR RENDER)
# ======================
PORT = int(os.environ.get("PORT", 10000))

async def start():
    await client.start()
    print("✅ Telegram Ready")


if __name__ == "__main__":
    tg_loop.run_until_complete(start())

    Thread(
        target=lambda: app.run(host="0.0.0.0", port=PORT),
        daemon=True
    ).start()

    tg_loop.run_forever()
