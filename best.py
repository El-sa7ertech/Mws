import asyncio
from flask import Flask, request
from telethon import TelegramClient, events
from threading import Thread
import os

print("🚀 Starting...")

# ======================
# Environment variables
# ======================
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")

print("API:", api_id, api_hash)

# ======================
# Telegram
# ======================
client = TelegramClient("session", api_id, api_hash)

# loop خاص بالـ Telegram
tg_loop = asyncio.new_event_loop()

async def start_bot():
    print("🤖 Telegram starting...", flush=True)

    await client.start()
    print("✅ Telegram Connected", flush=True)

    # استقبال الرسائل
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
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running ✅"

# إرسال رسالة من المتصفح
@app.route("/send")
def send():
    text = request.args.get("msg", "Hello")

    print("📤 Sending:", text, flush=True)

    future = asyncio.run_coroutine_threadsafe(
        client.send_message("me", text),
        tg_loop
    )

    try:
        future.result()  # مهم عشان ينفذ فعلياً
    except Exception as e:
        print("❌ ERROR:", e, flush=True)

    return "Sent ✅"

# ======================
# تشغيل Telegram مباشرة (مهم!)
# ======================
Thread(target=run_telegram, daemon=True).start()
