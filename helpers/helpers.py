import telebot
from config.config import BOT_TOKEN , ADMIN_CHAT_ID
from helpers.extraHelpers import  send_welcome_admin

bot = telebot.TeleBot(BOT_TOKEN)

def send_welcome_helper(message):
    if message.chat.id == ADMIN_CHAT_ID:
        send_welcome_admin(message, bot)
    else:
        send_welcome_admin(message, bot)


from config.config import BOT_TOKEN

bot = telebot.TeleBot(BOT_TOKEN)


def handle_contact_helper(message):
    chat_id = message.chat.id
    contact = message.contact
    phone_number = contact.phone_number
    first_name = contact.first_name
    last_name = contact.last_name

    if phone_number[0] != "+":
        phone_number = "+" + phone_number

