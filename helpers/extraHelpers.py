from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telethon import TelegramClient, errors


async def send_message(message, bot, messageField):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    contact_button = KeyboardButton("📞 Send Contact", request_contact=True)
    markup.add(contact_button)
    await bot.send_message(message.chat.id, messageField, reply_markup=markup)


async def send_welcome_admin(message, bot):
    name = message.from_user.first_name
    welcome_message = f"""
Salom {name}. Siz tizimda admin rolidasiz.
    """
    await bot.send_message(message.chat.id, welcome_message)


api_id = '20182242'
api_hash = '7546947bc9764e8bfbc05918189fb608'


async def check_exist_in_required_channel(chat_id, channels):
    async with TelegramClient('bot_session', int(api_id), api_hash) as client:
        membership_status = []

        for channel in channels:
            try:
                participants = await client.get_participants(channel)
                is_member = any(participant.id == chat_id for participant in participants)
                membership_status.append(is_member)

            except Exception as e:
                print(f"Error checking {channel}: {e}")
                membership_status.append(False)

        return all(membership_status)
