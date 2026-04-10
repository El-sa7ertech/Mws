import os
import asyncio
from flask import Flask
from telethon import TelegramClient

# ======================
# إعداد Telegram
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
# تشغيل Telegram
# ======================
async def start_bot():
    await client.start()
    print("✅ Telegram Connected", flush=True)

    user = "Aminabdalbdea"
    msg = "اشتغل"

    await client.send_message(user, msg)
    print("تم إرسال الرسالة!")

# ======================
# تشغيل السيرفر
# ======================
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(start_bot())

    PORT = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)
