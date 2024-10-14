import csv
import asyncio
from telethon import TelegramClient, functions, types

# Replace these with your own credentials
api_id = "29134217"
api_hash = "a84c6fcaf6a37bf92c0dbb4e9c86c758"
phone_number = "+919316141201"

async def get_unread_messages_from_user(client, username):
    try:
        user = await client.get_entity(username)
        result = await client(functions.messages.GetHistoryRequest(
            peer=user,
            limit=100,  # Adjust as needed
            offset_date=None,
            offset_id=0,
            max_id=0,
            min_id=0,
            add_offset=0,
            hash=0
        ))

        unread_messages = []
        for message in result.messages:
            if not message.out and message.is_read is False:
                unread_messages.append(message.message)
        
        return unread_messages

    except Exception as e:
        print(f'Error retrieving messages from {username}: {e}')
        return []

async def main(input_csv_path, output_csv_path):
    # Create the client and connect
    client = TelegramClient('session_name', api_id, api_hash)

    async with client:
        await client.start(phone_number)

        # Read usernames from the input CSV file
        with open(input_csv_path, mode='r') as file:
            reader = csv.reader(file)
            usernames = [row[0] for row in reader]

        # Open the output CSV file for writing
        with open(output_csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['username', 'unread_messages'])

            users_to_remove = []

            # Iterate over usernames and fetch unread messages from each user
            for username in usernames:
                unread_messages = await get_unread_messages_from_user(client, username)
                writer.writerow([username, unread_messages])

                # Print unread messages to the terminal
                print(f'Unread messages for {username}:')
                for msg in unread_messages:
                    print(msg)
                print('---')

                # If there are no unread messages, mark user for removal
                if not unread_messages:
                    users_to_remove.append(username)

        # Remove processed usernames from the original CSV
        remaining_usernames = [username for username in usernames if username not in users_to_remove]

        with open(input_csv_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            for username in remaining_usernames:
                writer.writerow([username])

if __name__ == '__main__':
    input_csv_path = 'sent_users.csv'  # Path to the CSV file containing usernames
    output_csv_path = 'unread_messages.csv'  # Path to the output CSV file for unread messages
    asyncio.run(main(input_csv_path, output_csv_path))
