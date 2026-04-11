import asyncio
from flask import Flask, request
from telethon import TelegramClient, events
from threading import Thread
from queue import Queue
import os

# ===== ENV =====
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")

# ===== Flask =====
app = Flask(__name__)

# ===== Telegram =====
client = TelegramClient("session", api_id, api_hash)

# ===== Queue =====
msg_queue = Queue()


# ======================
# Telegram Bot
# ======================
async def telegram_worker():
    print("🚀 Telegram worker started", flush=True)

    await client.start()
    print("✅ Telegram Connected", flush=True)

    # listener (اختياري)
    @client.on(events.NewMessage)
    async def handler(event):
        print("📩", event.text, flush=True)

    # worker loop
    while True:
        text = await asyncio.to_thread(msg_queue.get)
        print("📤 Sending:", text, flush=True)

        await client.send_message("Aminabdalbdea", text)


def run_telegram():
    asyncio.run(telegram_worker())


# ======================
# Flask Routes
# ======================
@app.route("/")
def home():
    return "Bot is running ✅"


@app.route("/send")
def send():
    text = request.args.get("msg", "Hello")

    msg_queue.put(text)

    print("📥 Queued:", text, flush=True)

    return "✅ Added to queue"


# ======================
# START TELEGRAM THREAD
# ======================
Thread(target=run_telegram, daemon=True).start()        print("📩", event.text, flush=True)

    # ✔️ إرسال بعد الاستقرار الكامل
    await client.send_message("Aminabdalbdea", "amin")

    tg_ready = True
    print("✅ Telegram Ready", flush=True)

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

    # ✔️ استخدام loop الخاص بالـ event thread
    asyncio.run_coroutine_threadsafe(
        client.send_message("Aminabdalbdea", text),
        asyncio.get_event_loop()
    )

    return "✅ Sent"


# ======================
# START TELEGRAM THREAD
# ======================
Thread(target=run_telegram, daemon=True).start()    async def handler(event):
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
