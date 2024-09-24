from telebot.async_telebot import AsyncTeleBot

from config.config import BOT_TOKEN, ADMIN_CHAT_ID
from helpers.extraHelpers import send_welcome_admin, send_message, check_exist_in_required_channel, save_contact_to_db, \
    check_user_exist_phone_number, check_user_exist_by_chat_id, get_result_by_code

bot = AsyncTeleBot(BOT_TOKEN)


async def send_welcome_helper(message):
    chat_id = message.chat.id
    first_name = message.from_user.first_name

    if str(chat_id) == ADMIN_CHAT_ID:
        await send_welcome_admin(message, bot)
    else:
        greeting_text = (f"Assalomu alaykum {first_name}, alpha academy botga xush kelibsiz. "
                         f"<code>Malumotlaringiz tekshirilmoqda .....</code>")
        await send_message(message, bot, greeting_text, False)
        check = await check_exist_in_required_channel(chat_id, ["abdulazizomonovblog", "sh0kh_07"])
        if check:
            if check_user_exist_by_chat_id(chat_id):
                await  send_message(message, bot,
                                    "Hammasi Joyida. Endi sizga taqdim etilgan <code>codeni</code> yuboring va natijangizni bilib oling!!",
                                    False)
                return
            await  send_message(message, bot, "Natijalarni olish uchun iltimos telefon raqamingizni ulashing.", True)
        else:
            await send_message(message, bot, """
Iltimos belgilangan kanallarni barchasiga ulaning va qaytadan /start bosing!!
<code>1.</code> @abdulazizomonovblog
<code>2.</code> @sh0kh_07
            """, False)


async def handle_contact_helper(message):
    chat_id = message.chat.id
    contact = message.contact
    phone_number = contact.phone_number
    first_name = contact.first_name
    last_name = contact.last_name

    if phone_number[0] != "+":
        phone_number = "+" + phone_number
    if not check_user_exist_phone_number(phone_number):
        save_contact_to_db(chat_id, phone_number, first_name, last_name)
    await send_message(message, bot,
                       "Hammasi Joyida. Endi sizga taqdim etilgan <code>codeni</code> yuboring va natijangizni bilib oling!!",
                       False)


async def handle_code(message):
    text = message.text
    result_text, markup = get_result_by_code(text)
    if markup:
        await bot.send_message(message.chat.id, result_text, reply_markup=markup, parse_mode="HTML")
    else:
        await bot.send_message(message.chat.id, result_text, parse_mode="HTML")
