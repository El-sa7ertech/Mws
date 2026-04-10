import os
import asyncio
from flask import Flask
from telethon import TelegramClient
from threading import Thread

print("9")

# ✅ إصلاح env (Case Sensitive)
api_id = int(os.environ.get("api_id"))
api_hash = os.environ.get("api_id")

print(api_id, api_hash)

app = Flask(__name__)
print(15)

@app.route("/")
def home():
    return "Bot is running ✅"

# ======================
# Telegram
# ======================

def run_telegram():
    print("🔥 Thread started", flush=True)

    try:
        # ✅ إنشاء loop داخل thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # ✅ إنشاء client داخل thread (مهم جدًا)
        client = TelegramClient("session", api_id, api_hash)

        async def start_bot():
            print("🚀 start_bot called", flush=True)
            print("🔥 Thread started")

            await client.start()
            print("✅ Telegram Connected", flush=True)

            await client.send_message("me", "Bot started 🚀")

            # ✅ مهم حتى لا يتوقف
            await client.run_until_disconnected()

        loop.run_until_complete(start_bot())

    except Exception as e:
        print("❌ ERROR:", e, flush=True)

# ======================
# MAIN
# ======================

if __name__ == "__main__":
    Thread(target=run_telegram, daemon=True).start()

    print("🌐 Flask starting...", flush=True)

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
