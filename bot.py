import telebot
from telebot import types
from config import config, test_config
from db_functions import *


def bot_app(test=False):
    if not test:
        context = config
    else:
        context = test_config

    bot = telebot.TeleBot(context.token)

    @bot.message_handler(commands=['start'])
    def start(message):
        markup = types.InlineKeyboardMarkup()
        for i in get_types(test):
            markup.row(types.InlineKeyboardButton(i['type'], callback_data=f'type_{i['id']}'))

        bot.reply_to(message, "Здравствуйте! Выберите вид блюда:", reply_markup=markup)

    bot.polling(non_stop=True, interval=0)


