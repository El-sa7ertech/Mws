import os
import asyncio
from flask import Flask
from telethon import TelegramClient
from threading import Thread

api_id = 
api_hash = "your_api_hash"
import os

api_id = int(os.environ.get("api_id"))
api_hash = os.environ.get("api_hash")
client = TelegramClient("session", api_id, api_hash)

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running ✅"

# ======================
# Telegram
# ======================
async def start_bot():
    print("🚀 start_bot called", flush=True)

    await client.start()
    print("✅ Telegram Connected", flush=True)

    await client.send_message("me", "Bot started 🚀")

    await client.run_until_disconnected()

def run_telegram():
    print("🔥 Thread started", flush=True)
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_bot())
    except Exception as e:
        print("❌ ERROR:", e, flush=True)

# ======================
# MAIN
# ======================
if __name__ == "__main__":
    Thread(target=run_telegram).start()

    print("🌐 Flask starting...", flush=True)

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
