from telebot import types, TeleBot
from dynaconf import settings as _settings
import pyowm


bot = TeleBot(_settings.SECRET_KEY)

keyboard = types.InlineKeyboardMarkup()
key_yes = types.InlineKeyboardButton(text='Что у нас по погоде?', callback_data='weather')
keyboard.add(key_yes)
key_no = types.InlineKeyboardButton(text='Пока не надо', callback_data='bye')
keyboard.add(key_no)


@bot.message_handler(commands=["weather"])
def weather_handler(message):
    chat_id = message.chat.id
    city = bot.send_message(chat_id, "В каком городе Вам показать погоду?")
    bot.register_next_step_handler(city, weather)


def weather(message):
    chat_id = message.chat.id
    city = message.text.lower()
    owm = pyowm.OWM(_settings.API_KEY, language="ru")
    city_weather = owm.weather_at_place(city)
    w = city_weather.get_weather()
    temperature = w.get_temperature("celsius")["temp"]
    wind = w.get_wind()["speed"]
    hum = w.get_humidity()
    desc = w.get_detailed_status()
    bot.send_message(
        chat_id,
        "Сейчас в городе "
        + str(city)
        + " "
        + str(desc)
        + ", температура - "
        + str(temperature)
        + "°C, влажность - "
        + str(hum)
        + "%, скорость ветра - "
        + str(wind)
        + "м/с.",
    )


@bot.message_handler(commands=["start", "go"])
def start_message(message):
    chat_id = message.chat.id
    user_name = message.from_user.first_name
    bot.send_message(
        chat_id,
        f"Приветствую вас, {user_name}!\n"
        f"Я бот, которй сообщит вам погоду в нужном для вас городе.\n"
        f"Для этого просто нажмите соответствующую кнопку.",
        reply_markup=keyboard,
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "weather":
        bot.send_message(call.message.chat.id, "Для того, чтобы узнать погоду введите /weather")
    else:
        bot.send_message(call.message.chat.id, "Чтобы воспользоваться мной еще раз, то просто нажмите /start")


if __name__ == "__main__":
    bot.polling(none_stop=True)
