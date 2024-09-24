import os
from io import BytesIO

import asyncpg
from telebot.async_telebot import AsyncTeleBot

from config.config import BOT_TOKEN, ADMIN_CHAT_ID, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB
from helpers.extraHelpers import send_welcome_admin, send_message, check_exist_in_required_channel, save_contact_to_db, \
    check_user_exist_phone_number, check_user_exist_by_chat_id, get_result_by_code, import_result_informations

bot = AsyncTeleBot(BOT_TOKEN)

allowed_extensions = ['.xls', '.xlsx']


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


async def handle_document_excel(message):
    document = message.document
    file_name = document.file_name
    file_extension = os.path.splitext(file_name)[1].lower()

    if file_extension in allowed_extensions:
        await bot.send_message(message.chat.id,
                               "<code>Malumotlar import qilinmoqda iltimos javobni kuting ......</code>",
                               parse_mode="HTML")

        file_id = document.file_id
        file = await bot.get_file(file_id)

        file_data = await bot.download_file(file.file_path)

        excel_file = BytesIO(file_data)

        await import_result_informations(excel_file, message.chat.id, bot)

    else:
        await bot.send_message(message.chat.id, "No, this is not an Excel file.")


async def handle_result(message):
    chat_id = message.chat.id
    result_text = message.text.strip()

    result_lines = result_text.split("\n")

    conn = await asyncpg.connect(user=POSTGRES_USER, password=POSTGRES_PASSWORD,
                                 database=POSTGRES_DB, host=POSTGRES_HOST)

    try:
        for line in result_lines:
            result_data = [item.strip() for item in line.split(",")]

            if len(result_data) != 5:
                await bot.send_message(chat_id, f"Invalid format in line: {line}")
                continue

            try:
                code = result_data[0]
                math_ball = int(result_data[1])
                english_ball = int(result_data[2])
                user_name = result_data[3]
                user_surname = result_data[4]
            except ValueError:
                await bot.send_message(chat_id, f"Invalid number format in line: {line}")
                continue

            try:
                await conn.execute('''
                    INSERT INTO results (code, math_ball, english_ball, user_name, user_surname)
                    VALUES ($1, $2, $3, $4, $5)
                    ON CONFLICT (code) DO NOTHING;
                ''', code, math_ball, english_ball, user_name, user_surname)

            except Exception as e:
                await bot.send_message(chat_id, f"Error inserting line: {line}. Error: {str(e)}")
                continue

        await bot.send_message(chat_id, "Natijalar muvaffaqiyatli qo'shildi.")

    finally:
        await conn.close()
