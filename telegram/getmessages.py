from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import PeerUser, PeerChat, PeerChannel

# Replace these with your own values
api_id = "29134217"
api_hash = "a84c6fcaf6a37bf92c0dbb4e9c86c758"
phone_number = "+919316141201"

client = TelegramClient('session_name', api_id, api_hash)

async def main():
    await client.start(phone=phone_number)
    print("Client Created")

    # Get your own user information
    me = await client.get_me()
    print(me.stringify())

    # Getting all dialogs (conversations/chats)
    async for dialog in client.iter_dialogs():
        print(dialog.name, 'has ID', dialog.id)
        
        # Fetching message history for each dialog
        if isinstance(dialog.entity, (PeerUser, PeerChat, PeerChannel)):
            history = await client(GetHistoryRequest(
                peer=dialog.entity,
                limit=10,  # You can adjust the limit as needed
                offset_date=None,
                offset_id=0,
                max_id=0,
                min_id=0,
                add_offset=0,
                hash=0
            ))
            for message in history.messages:
                print(f"Message in {dialog.name}: {message.message}")

with client:
    client.loop.run_until_complete(main())
