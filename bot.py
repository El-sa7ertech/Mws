import asyncio
import os
from telethon import TelegramClient

api_id = int(os.environ["api_id"])
api_hash = os.environ["api_hash"]

client = TelegramClient("session", api_id, api_hash)

async def main():
    await client.start()

    user = "aminabdalbdea"
    msg = "اشتغل من Render 🚀"

    await client.send_message(user, msg)

    print("تم إرسال الرسالة!")

    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
