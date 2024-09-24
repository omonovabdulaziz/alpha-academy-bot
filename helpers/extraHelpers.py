import asyncpg
import pandas as pd
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telethon import TelegramClient

from config.config import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB
from database.postgres import get_db_connection


async def send_message(message, bot, messageField, state):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    contact_button = KeyboardButton("📞 Telefon raqam yuborish", request_contact=True)
    markup.add(contact_button)
    if state:
        await bot.send_message(message.chat.id, messageField, reply_markup=markup)
    else:
        await bot.send_message(message.chat.id, messageField, parse_mode="HTML")


async def send_welcome_admin(message, bot):
    name = message.from_user.first_name
    welcome_message = f"""
    Salom {name}. Siz tizimda <code>admin</code> rolidasiz, kerakli amalni tanlang.
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    import_button = KeyboardButton("Natijalarni Yuklash (Excel orqali)")
    add_result_button = KeyboardButton("Natija qo'shish")
    add_competition_button = KeyboardButton("Yangi Musobaqa qo'shish")

    markup.add(import_button, add_result_button)
    markup.add(add_competition_button)
    await bot.send_message(message.chat.id, welcome_message, reply_markup=markup, parse_mode='HTML')


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


def save_contact_to_db(chat_id, phone_number, first_name, last_name):
    conn = get_db_connection()
    cur = conn.cursor()

    try:
        cur.execute("""
            INSERT INTO users (chat_id, phone_number, first_name, last_name)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (chat_id) DO UPDATE SET
                phone_number = EXCLUDED.phone_number,
                first_name = EXCLUDED.first_name,
                last_name = EXCLUDED.last_name;
        """, (chat_id, phone_number, first_name, last_name))

        conn.commit()
    except Exception as e:
        print(f"Error saving contact to database: {e}")
    finally:
        cur.close()
        conn.close()


def check_user_exist_phone_number(phone_number):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM users WHERE phone_number = %s", (phone_number,))
        count = cur.fetchone()[0]
        return count > 0
    except Exception as e:
        print(f"Error checking phone number: {e}")
        return False
    finally:
        cur.close()
        conn.close()


def check_user_exist_by_chat_id(chat_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT COUNT(*) FROM users WHERE chat_id = %s", (chat_id,))
        count = cur.fetchone()[0]
        return count > 0
    except Exception as e:
        print(f"Error checking chat_id : {e}")
        return False
    finally:
        cur.close()
        conn.close()


def get_result_by_code(code):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT code, math_ball, english_ball FROM results WHERE code = %s", (code,))
        result = cur.fetchone()
        if result:
            message_text = f"""
<code>1. Sizning codingiz: </code> {result[0]}
<code>2. Matematika ballingiz: </code> {result[1]}
<code>3. Ingliz tili ballingiz: </code> {result[2]}
<code>4. Umumiy ballingiz: </code> {result[1] + result[2]}
            """
            markup = InlineKeyboardMarkup()
            download_button = InlineKeyboardButton("📄 Sertifikatni yuklab olish",
                                                   callback_data=f'download_certificate_{result[0]}')
            markup.add(download_button)

            return message_text, markup
        else:
            return f"No result found for code: {code}", None
    except Exception as e:
        return f"Error while getting code: {str(e)}", None
    finally:
        cur.close()
        conn.close()


async def import_result_informations(file_stream, chat_id, bot):
    df = pd.read_excel(file_stream)

    conn = await asyncpg.connect(user=POSTGRES_USER, password=POSTGRES_PASSWORD,
                                 database=POSTGRES_DB, host=POSTGRES_HOST)
    try:
        for index, row in df.iterrows():
            await conn.execute('''
                INSERT INTO results (code, math_ball, english_ball, user_name, user_surname)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (code) DO NOTHING;
            ''', row['code'], row['math_ball'], row['english_ball'], row['user_name'], row['user_surname'])
    finally:
        await conn.close()

    await bot.send_message(chat_id=chat_id, text="Malumotlar muvaffaqiyatli import qilindi.")
