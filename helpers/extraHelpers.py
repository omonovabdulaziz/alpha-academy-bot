from telebot.types import ReplyKeyboardMarkup, KeyboardButton


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
