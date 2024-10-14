from telethon.sync import TelegramClient, events
import csv
import os

# Load your Telegram API credentials
api_id = "29134217"
api_hash = "a84c6fcaf6a37bf92c0dbb4e9c86c758"
bot_token = "7031110269:AAEDtiy-8QGUIsw2CIbBN4SJx7Qmb7zTR0Y"

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

# Create a set to store unique user information
unique_users = set()

def save_to_csv(users, filename):
    if not users:
        print("No users found.")
        return None

    keys = users[0].keys()
    file_exists = os.path.isfile(filename)
    with open(filename, 'a', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        if not file_exists:
            dict_writer.writeheader()
        dict_writer.writerows(users)
    return filename

@client.on(events.NewMessage(chats=['Oppenheimer_Tamil_Telugu_Movie']))  # Replace with public group usernames
async def handler(event):
    sender = await event.get_sender()
    user = {
        'id': sender.id,
        'username': sender.username,
        'first_name': sender.first_name,
        'last_name': sender.last_name
    }

    # Only add new users to the set
    if user['id'] not in unique_users:
        unique_users.add(user['id'])
        save_to_csv([user], 'all_users.csv')
        print(f"User {user['username']} added to CSV.")

if __name__ == '__main__':
    print("Listening to messages in public groups...")
    client.run_until_disconnected()
