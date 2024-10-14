import csv
from telethon import TelegramClient
import asyncio
from datetime import datetime, timedelta, timezone

api_id = "29134217"
api_hash = "a84c6fcaf6a37bf92c0dbb4e9c86c758"
phone_number = "+919316141201"  # replace with your actual phone number (string)

# Create the client and connect
client = TelegramClient('session_name', api_id, api_hash)

async def check_recent_unread_replies(target_username):
    await client.start(phone_number)
    me = await client.get_me()

    now = datetime.now(timezone.utc)
    twenty_minutes_ago = now - timedelta(minutes=20)
    reply_to_message = None
    messages=[]

    async for dialog in client.iter_dialogs(limit=4):
        print(dialog)
        if dialog.is_user and dialog.unread_count > 0 and dialog.entity.username == target_username:
            # print(dialog)
            async for message in client.iter_messages(dialog.id, limit=4):
                reply_to_message = message
                messages.append({
                    "username":target_username,
                    "message":message.message,
                })
                
                if reply_to_message.media_unread==True:
                    break
                
                continue
            
            
    await client.disconnect()

    if reply_to_message:
        print(f"Unread reply from @{target_username} : {messages}")
    else:
        print(f"No unread replies from @{target_username} in the last 20 minutes.")

def get_target_usernames_from_csv(csv_file):
    usernames = []
    with open(csv_file, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            usernames.append(row[0])
    return usernames

# Run the function
if __name__ == '__main__':
    csv_file = 'sent_users.csv'  # Path to your CSV file
    target_usernames = get_target_usernames_from_csv(csv_file)
    
    # if target_usernames:
    #     for username in target_usernames:
    asyncio.run(check_recent_unread_replies("tushar_sharma07"))
    # else:
        # print("No target usernames found in the CSV file.")

