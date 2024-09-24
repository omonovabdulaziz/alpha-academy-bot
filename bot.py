from config.config import IS_MIGRATE
from database.postgres import create_tables
from helpers.helpers import handle_contact_helper, bot, send_welcome_helper


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    handle_contact_helper(message)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    send_welcome_helper(message)


if __name__ == '__main__':
    print("Bot listening....")
    if IS_MIGRATE:
        create_tables()

    bot.polling(none_stop=True)
