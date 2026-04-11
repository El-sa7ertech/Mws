import asyncio
from flask import Flask, request
from telethon import TelegramClient, events
from threading import Thread
import os

print("9")

api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")

client = TelegramClient("session", api_id, api_hash)

print(api_id, api_hash)

app = Flask(__name__)

print(15)

# ======================
# Telegram loop
# ======================
tg_loop = asyncio.new_event_loop()

async def start_bot():
    print("🚀 start_bot called", flush=True)

    await client.start()
    print("✅ Telegram Connected", flush=True)

    @client.on(events.NewMessage)
    async def handler(event):
        print("📩", event.text, flush=True)

    await client.run_until_disconnected()

def run_telegram():
    print("🔥 Thread started", flush=True)

    asyncio.set_event_loop(tg_loop)
    tg_loop.run_until_complete(start_bot())

# ======================
# Flask
# ======================
@app.route("/")
def home():
    return "Bot is running ✅"

@app.route("/send")
def send():
    text = request.args.get("msg", "Hello")
    print("🔥 sent", text, flush=True)

    # ✅ تأكد أن الكلاينت شغال
    if not client.is_connected():
        return "❌ Telegram not connected"

    # ✅ إرسال بدون انتظار (بدون result)
    asyncio.run_coroutine_threadsafe(
        client.send_message("me", text),
        tg_loop
    )

    return "Sent ✅"

# ======================
# MAIN
# ======================
if __name__ == "__main__":
    Thread(target=run_telegram, daemon=True).start()

    print("🌐 Flask starting...", flush=True)

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
