import asyncio
import os
from telethon import TelegramClient

api_id = int(os.environ.get("api_id"))
api_hash = os.environ.get("api_hash")

client = TelegramClient("session", api_id, api_hash)

async def main():
    print("🚀 Telegram starting...")

    await client.start()
    print("✅ Telegram Connected")

    await client.send_message("Aminabdalbdea", "Bot started 🚀")

    await client.run_until_disconnected()

asyncio.run(main())
