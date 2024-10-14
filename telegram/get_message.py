import csv
import asyncio
from telethon import TelegramClient
from datetime import datetime, timedelta, timezone
api_id = "25009798"
api_hash = "69850bfa0d9755588ba312035d0e5947"
phone_number = "+918562800573"

def store_messages_to_csv(target_username, messages, csv_filename='messages.csv'):
    # Open the CSV file in append mode
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        # Write the target username and messages to the CSV file
        writer.writerow([target_username, messages])

async def check_recent_unread_replies(target_username, client):
    await client.start(phone_number)
    me = await client.get_me()

    now = datetime.now(timezone.utc)
    twenty_minutes_ago = now - timedelta(minutes=20)
    reply_to_message = None
    messages = []

    async for dialog in client.iter_dialogs(limit=4):
        if dialog.is_user and dialog.unread_count > 0 and dialog.entity.username == target_username:
            async for message in client.iter_messages(dialog.id, limit=4):
                reply_to_message = message
                print(message)
                messages.append({
                    "username":target_username,
                    "message":message.message,
                })
                
                if reply_to_message.media_unread==False:
                    break
                
                continue
            
            
    # await client.disconnect()
    if reply_to_message:
        print(f"Unread reply from @{target_username} : {messages}")
        store_messages_to_csv(target_username, message)

    else:
        print(f"No unread replies from @{target_username} in the last 20 minutes.")

async def get_target_usernames_from_csv(csv_file):
    usernames = []
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip the header
        for row in reader:
            if row:
                usernames.append(row[0])
    return usernames

async def main():
    csv_file = 'sent_users.csv'  # Path to your CSV file
    target_usernames = await get_target_usernames_from_csv(csv_file)

    # Create a Telegram client
    client = TelegramClient('session_name', api_id, api_hash)

    await client.connect()

    try:
        tasks = [check_recent_unread_replies(username, client) for username in target_usernames]
        await asyncio.gather(*tasks)
    finally:
        await client.disconnect()

# Run the function
if __name__ == '__main__':
    asyncio.run(main())
