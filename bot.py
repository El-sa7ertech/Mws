import asyncio
from telethon import TelegramClient, events

api_id = int(os.environ.get("api_id"))
api_hash = os.environ.get("api_hash")
client = TelegramClient("session", api_id, api_hash)



async def main():
    
    await client.start()
    await client.send_message("Aminabdalbdea", "اشتغل")
    print("Bot is running...")
    await client.run_until_disconnected()

asyncio.run(main())
