from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telethon import TelegramClient

def send_message(message, bot):
    name = message.from_user.first_name

    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    contact_button = KeyboardButton("📞 Send Contact", request_contact=True)
    markup.add(contact_button)
    welcome_message = f"""
🇺🇿
Salom {name} 👋
Natijalarni bilish uchun contactingizni yuboring va kodingizni kiritib natijalaringiz haqida bilib oling.
    """
    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)


def send_welcome_admin(message, bot):
    name = message.from_user.first_name
    welcome_message = f"""
Salom {name}. Siz tizimda admin rolidasiz.
    """
    bot.send_message(message.chat.id, welcome_message)


api_id = '20182242'
api_hash = '7546947bc9764e8bfbc05918189fb608'

async def check_exist_in_required_channel(chat_id, required_channels):
    async with TelegramClient('bot_session', int(api_id), api_hash) as client:
        try:
            for channel in required_channels:
                participant = await client.get_participant(channel, chat_id)
                if participant:
                    return True
            return False
        except Exception as e:
            print(f"Xato: {e}")
            return False


def handle_check_channel_subscription(message, bot):
    required_channels = ['channel1', 'channel2']
    chat_id = message.chat.id

    import asyncio
    if asyncio.run(check_exist_in_required_channel(chat_id, required_channels)):
        bot.send_message(chat_id, "Siz kerakli kanallarga obuna bo'ldingiz.")
    else:
        bot.send_message(chat_id, "Siz kerakli kanallarga obuna bo'lmagansiz.")