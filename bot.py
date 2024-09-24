from config.config import IS_MIGRATE
from database.postgres import create_tables
from helpers.helpers import handle_contact_helper, bot, send_welcome_helper, handle_code
import asyncio


@bot.message_handler(content_types=['contact'])
async def handle_contact(message):
    await handle_contact_helper(message)


@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await send_welcome_helper(message)


@bot.message_handler(content_types=['text'])
async def handle_any_message(message):
    await handle_code(message)


if __name__ == '__main__':
    print("Bot listening....")
    if IS_MIGRATE:
        create_tables()

    asyncio.run(bot.polling())
