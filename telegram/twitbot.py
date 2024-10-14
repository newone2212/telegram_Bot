from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch
import csv
import os

# Load your Telegram API credentials from environment variables
api_id = "29134217"
api_hash = "a84c6fcaf6a37bf92c0dbb4e9c86c758"
bot_token = "7031110269:AAEDtiy-8QGUIsw2CIbBN4SJx7Qmb7zTR0Y"

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

async def scrape_users(channel_username):
    offset = 0
    limit = 100
    all_participants = []

    while True:
        participants = await client(GetParticipantsRequest(
            channel=channel_username,
            filter=ChannelParticipantsSearch(''),
            offset=offset,
            limit=limit,
            hash=0
        ))
        
        if not participants.users:
            break
        
        all_participants.extend(participants.users)
        offset += len(participants.users)

    users = []
    for participant in all_participants:
        user = {
            'id': participant.id,
            'username': participant.username,
            'first_name': participant.first_name,
            'last_name': participant.last_name
        }
        users.append(user)
    return users

def save_to_csv(users, channel_username):
    if not users:
        print("No users found.")
        return None

    filename = f"{channel_username}_users.csv"
    keys = users[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(users)
    return filename

if __name__ == '__main__':
    try:
        import asyncio
        channel_username = 'TESTFORBOT012'  # Replace with the desired channel username
        users = client.loop.run_until_complete(scrape_users(channel_username))
        print(users)
        csv_file = save_to_csv(users, channel_username)
        if csv_file:
            print(f"Saved to {csv_file}")
    except  Exception as e:
        print(str(e))
