import telebot

bot = telebot.TeleBot('1084847822:AAFh2U1ORn6Vu-vEj8D9jh4J9XaD5xVM1TU')


keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Привет', 'Пока')
keyboard2 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard2.row('Как дела', 'Пока')


@bot.message_handler(commands=['start', 'go'])
def start_message(message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Ну что, начнем работу', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def text_handler(message):
    text = message.text.lower()
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    if text == "привет":
        bot.send_message(chat_id, f'Привет, {user_name}', reply_markup=keyboard2)
    elif text == "как дела":
        bot.send_message(chat_id, 'норм')
    else:
        bot.send_message(chat_id, 'пока')


if __name__ == '__main__':
    bot.polling(none_stop=True)
