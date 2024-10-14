import csv
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

# Replace this with your bot token
bot_token = "7031110269:AAEDtiy-8QGUIsw2CIbBN4SJx7Qmb7zTR0Y"

# Initialize bot and dispatcher
bot = Bot(token=bot_token)
dp = Dispatcher(bot)

# Path to the file where messages will be logged
log_file_path = 'message_log.csv'

# Ensure the log file exists
with open(log_file_path, 'a', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['username', 'message'])

@dp.message_handler()
async def handle_message(message: types.Message):
    username = message.from_user.username
    text = message.text
    
    # Log the message to the CSV file
    with open(log_file_path, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([username, text])
    
    # Respond to the user
    await message.answer("Message received")

async def main():
    # Start the bot
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
