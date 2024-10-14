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

async def main(message,username):
    # Create the client and connect
    client = TelegramClient('session_name', api_id, api_hash)

    # Read the CSV file and accumulate messages
    messages_to_send =message
    total_messages_sent = 0
    max_messages = 20
    # users_to_remove = []

    async with client:
        await client.start(phone_number)
        await send_message(client, username, message)
        
if __name__ == '__main__':
    username=input("enter usename:")
    message=input("enter message:")
      # Path to your CSV file
    asyncio.run(main(username=username,message=message))
