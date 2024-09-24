from helpers.helpers import handle_contact_helper, bot


@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    handle_contact_helper(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
