import asyncio
from flask import Flask, request
from telethon import TelegramClient, events
from threading import Thread
import os

print("9")

# ===== ENV =====
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")

print(api_id, api_hash)

# ===== Flask =====
app = Flask(__name__)

# ===== Telegram =====
client = TelegramClient("session", api_id, api_hash)
tg_ready = False


# ======================
# Telegram Bot
# ======================
async def start_bot():
    global tg_ready

    print("🚀 start_bot called", flush=True)

    await client.start()

    tg_ready = True
    print("✅ Telegram Connected", flush=True)

    @client.on(events.NewMessage)
    async def handler(event):
        print("📩", event.text, flush=True)

    await client.run_until_disconnected()


def run_telegram():
    asyncio.run(start_bot())


# ======================
# Flask Routes
# ======================
@app.route("/")
def home():
    return "Bot is running ✅"


@app.route("/send")
def send():
    text = request.args.get("msg", "Hello")

    print("📤 Sending:", text, flush=True)

    if not tg_ready:
        return "❌ Telegram not ready yet"

    asyncio.run_coroutine_threadsafe(
        client.send_message("Aminabdalbdea", text),
        client.loop
    )

    return "✅ Sent"


# ======================
# START TELEGRAM THREAD
# ======================
Thread(target=run_telegram, daemon=True).start()


# ======================
# IMPORTANT FOR RENDER (Gunicorn)
# ======================
# لازم يكون موجود app فقط بدون app.run()
