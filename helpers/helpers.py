import telebot


def handle_contact_helper(message):
    chat_id = message.chat.id
    contact = message.contact
    phone_number = contact.phone_number
    first_name = contact.first_name
    last_name = contact.last_name

    if phone_number[0] != "+":
        phone_number = "+" + phone_number
