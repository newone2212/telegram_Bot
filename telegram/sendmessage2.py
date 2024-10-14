import csv
import ast
import asyncio
from telethon import TelegramClient

# Replace these with your own credentials
api_id = "29134217"
api_hash = "a84c6fcaf6a37bf92c0dbb4e9c86c758"
phone_number = "+919316141201"

async def send_message(client, username, message):
    try:
        await client.send_message(username, message)
        print(f'Message sent to {username}: {message}')
    except Exception as e:
        print(f'Error sending message to {username}: {e}')

async def main(csv_file_path, sent_users_csv_path):
    # Create the client and connect
    client = TelegramClient('session_name', api_id, api_hash)

    # Read the CSV file and accumulate messages
    messages_to_send = []
    with open(csv_file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            username = row['username']
            messages_str = row['messages']
            messages_str = messages_str.replace('"', '').replace('[', '').replace(']', '')  # Remove brackets and extra quotes
            messages = messages_str.split(', ')  # Split the string into a list of messages
            messages_to_send.append((username, messages))

    total_messages_sent = 0
    max_messages = 20
    users_to_remove = []

    async with client:
        await client.start(phone_number)
        for username, messages in messages_to_send:
            if total_messages_sent >= max_messages:
                break

            all_messages_sent = True
            for message in messages:
                if total_messages_sent >= max_messages:
                    all_messages_sent = False
                    break
                if message.strip():  # Only send non-empty messages
                    await send_message(client, username, message)
                    total_messages_sent += 1
            
            if all_messages_sent:
                users_to_remove.append(username)

    # Move the usernames to the 'sent' CSV file before removing them from the original CSV
    with open(sent_users_csv_path, mode='a', newline='') as sent_file:
        sent_writer = csv.writer(sent_file)
        for username in users_to_remove:
            sent_writer.writerow([username])

    # Rewrite the CSV file excluding users whose messages were fully sent
    with open(csv_file_path, mode='r') as file:
        reader = list(csv.DictReader(file))
    with open(csv_file_path, mode='w', newline='') as file:
        fieldnames = reader[0].keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in reader:
            if row['username'] not in users_to_remove:
                writer.writerow(row)

if __name__ == '__main__':
    csv_file_path = 'send.csv'  # Path to your CSV file
    sent_users_csv_path = 'sent_users.csv'  # Path to the CSV file where sent usernames will be stored
    asyncio.run(main(csv_file_path, sent_users_csv_path))
