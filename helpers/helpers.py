import telebot
from config.config import BOT_TOKEN , ADMIN_CHAT_ID
from helpers.extraHelpers import  send_welcome_admin

bot = telebot.TeleBot(BOT_TOKEN)

def send_welcome_helper(message):
    if message.chat.id == ADMIN_CHAT_ID:
        send_welcome_admin(message, bot)
    else:
        send_welcome_admin(message, bot)