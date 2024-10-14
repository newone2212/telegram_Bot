from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest
from telethon.tl.types import ChannelParticipantsSearch, InputPeerChannel
import csv
import os

# Load your Telegram API credentials
api_id = "29134217"
api_hash = "a84c6fcaf6a37bf92c0dbb4e9c86c758"
phone_number = "+919316141201"

client = TelegramClient('session_name', api_id, api_hash)

async def scrape_users(channel_username):
    try:
        entity = await client.get_entity(channel_username)
        print(f"Entity details: {entity}")
        if not isinstance(entity, InputPeerChannel):
            print(f"Entity is of type: {type(entity).__name__}")
            raise TypeError("The provided username does not belong to a channel")

        offset = 0
        limit = 100
        all_participants = []

        while True:
            participants = await client(GetParticipantsRequest(
                channel=entity,
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
    except TypeError as te:
        print(f"Failed to get entity: {te}")
    except Exception as e:
        print(f"Failed to scrape users: {e}")
        return []

def save_to_csv(users, filename):
    if not users:
        print("No users found.")
        return None

    file_exists = os.path.isfile(filename)
    keys = users[0].keys()
    with open(filename, 'a', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        if not file_exists:
            dict_writer.writeheader()
        dict_writer.writerows(users)
    return filename

if __name__ == '__main__':
    import asyncio
    client.start(phone_number)  # Start the client and login using the phone number
    channel_usernames = ['TESTFORBOT012']  # Replace with desired channel usernames
    filename = 'all_users.csv'
    all_users_info = []

    for channel_username in channel_usernames:
        users = client.loop.run_until_complete(scrape_users(channel_username))
        if users:
            all_users_info.extend(users)

    if all_users_info:
        csv_file = save_to_csv(all_users_info, filename)
        if csv_file:
            print(f"Appended to {csv_file}")

    client.disconnect()
