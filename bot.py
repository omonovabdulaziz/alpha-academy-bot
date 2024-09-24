import asyncio

from config.config import IS_MIGRATE, ADMIN_CHAT_ID
from database.postgres import create_tables
from helpers.extraHelpers import check_exist_in_required_channel
from helpers.helpers import handle_contact_helper, bot, send_welcome_helper, handle_code, handle_document_excel, \
    handle_result


@bot.message_handler(commands=['start'])
async def send_welcome(message):
    await send_welcome_helper(message)


@bot.message_handler(content_types=['contact'])
async def handle_contact(message):
    await handle_contact_helper(message)


@bot.message_handler(func=lambda message: message.text == "Natijalarni Import Qilish (Excel orqali)")
async def handle_import_results(message):
    chat_id = message.chat.id
    if str(chat_id) != ADMIN_CHAT_ID:
        await bot.send_message(chat_id, "Forbidden 403")
        return
    await bot.send_message(chat_id, "<code>Excel File yuklanishi kutilmoqda .............. </code>", parse_mode="HTML")


@bot.message_handler(func=lambda message: message.text == "Natija qo'shish")
async def handle_add_result(message):
    chat_id = message.chat.id
    if str(chat_id) != ADMIN_CHAT_ID:
        await bot.send_message(chat_id, "Forbidden 403")
        return
    await bot.send_message(message.chat.id, """
    Yaxshi endi namunadagiday natijalarni yuboring. 
    Namuna:
<code>123234 , 12 , 12 , Abdulaziz , Omonov 
12323 , 34 , 45 , Shohrux , To'xtanazarov</code>
    
    
Namunadan nusxa oling va  har bir natijani qo'shishda bitta pastki qatorga tushushni unutmang !!
    """, parse_mode="HTML")


@bot.message_handler(func=lambda message: message.text == "Yangi Musobaqa qo'shish")
async def handle_add_competition(message):
    chat_id = message.chat.id
    if str(chat_id) != ADMIN_CHAT_ID:
        await bot.send_message(chat_id, "Forbidden 403")
        return
    await bot.send_message(message.chat.id, "Ushbu qism tamirda ⚒ ......")


@bot.message_handler(content_types=['text'])
async def handle_any_message(message):
    chat_id = message.chat.id
    if str(chat_id) == ADMIN_CHAT_ID:
        await handle_result(message)
    else:
        check = await check_exist_in_required_channel(chat_id, ["abdulazizomonovblog", "sh0kh_07"])
        if not check:
            bot.send_message(chat_id, "Iltimos talab qilingan kanallarga azo bo'ling !!")
            return
        await handle_code(message)


@bot.callback_query_handler(func=lambda call: call.data.startswith('download_certificate_'))
async def handle_download_certificate(call):
    code = call.data.split('_')[2]
    await bot.send_message(call.message.chat.id, "Sertifikatingiz tayyorlanmoqda iltimos kuting <code> 🕔 </code>",
                           parse_mode='HTML')


@bot.message_handler(content_types=['document'])
async def handle_document(message):
    await handle_document_excel(message)


if __name__ == '__main__':
    print("Bot listening....")
    if IS_MIGRATE:
        create_tables()

    asyncio.run(bot.polling())
