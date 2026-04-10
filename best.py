import os
import asyncio
from flask import Flask
from telethon import TelegramClient
from threading import Thread

# ======================
# Telegram
# ======================
api_id = 123456
api_hash = "your_api_hash"
bot_username = "mysudan1bot"

client = TelegramClient("session", api_id, api_hash)

# ======================
# Flask
# ======================
app = Flask(__name__)

@app.route("/")
def home():
    return "Telegram Bot Running ✅"

# ======================
# Telegram Task
# ======================
async def start_bot():
    await client.start()
    print("✅ Telegram Connected", flush=True)

    user = "Aminabdalbdea"
    msg = "اشتغل"

    await client.send_message(user, msg)
    print("تم إرسال الرسالة!", flush=True)

# تشغيل asyncio في Thread
def run_telegram():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(start_bot())

# ======================
# تشغيل السيرفر
# ======================
if __name__ == "__main__":
    Thread(target=run_telegram).start()

    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
