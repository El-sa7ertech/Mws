import asyncio
from telethon import TelegramClient, events

api_id = int(os.environ.get("api_id"))
api_hash = os.environ.get("api_hash")
client = TelegramClient("session", api_id, api_hash)

@client.on(events.NewMessage)
async def handler(event):
    print("📩", event.text)

    if event.text == "hi":
        await event.reply("Hello 👋")

async def main():
    await client.start()
    print("Bot is running...")
    await client.run_until_disconnected()

asyncio.run(main())
