import telebot
from telebot import types
from config import config, test_config
from db_functions import *
import random


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
            markup.row(types.InlineKeyboardButton(i['type'], callback_data=f'type_{i["id"]}'))

        bot.reply_to(message, "Здравствуйте! Выберите вид блюда:", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call: True)
    def test_callback(call):
        if call.data.split('_')[0] == 'type':
            type_id = call.data.split('_')[1]
            markup = types.InlineKeyboardMarkup()
            markup.row(types.InlineKeyboardButton('Случайное блюдо', callback_data=f'random_{type_id}'))
            markup.row(types.InlineKeyboardButton('Все блюда', callback_data=f'all_{type_id}'))
            bot.send_message(call.message.chat.id, 'Выберете метод отображения', reply_markup=markup)
        if call.data.split("_")[0] in ('all', 'random'):
            show_dish(call, call.data.split("_")[1], call.data.split("_")[0])
        if call.data.isdigit():
            show_dish(call, int(call.data), 'show')



    def show_dish(call, id, method):
        list_ = get_dish_name_by_type(id, test)
        if method == 'random':
            dish = random.choice(list_)

            markup = types.ReplyKeyboardMarkup()
            markup.add(types.KeyboardButton('Вернуться назад'))
            bot.send_photo(call.message.chat.id, dish['photo_id'], caption=f'{dish["name"]} \n {dish["ingredients"]}')
            bot.send_message(call.message.chat.id, dish['recipe'], reply_markup=markup)
        if method == 'all':
            markup = types.InlineKeyboardMarkup()
            for dish in list_:
                markup.row(types.InlineKeyboardButton(dish['name'], callback_data=dish['id']))
            bot.send_message(call.message.chat.id, "Выберите блюдо", reply_markup=markup)

        if method == "show":
            dish = get_dish_by_id(id, test)[0]
            markup = types.ReplyKeyboardMarkup()
            markup.add(types.KeyboardButton('Вернуться назад'))
            bot.send_photo(call.message.chat.id, dish['photo_id'], caption=f'{dish["name"]} \n {dish["ingredients"]}')
            bot.send_message(call.message.chat.id, dish['recipe'], reply_markup=markup)

    @bot.message_handler(commands=['admin'])
    def admin_start(message):
        if message.from_user.username in get_admins(test)['all_admins']:
            markup = types.ReplyKeyboardMarkup()
            markup.add(types.KeyboardButton('Добавить блюдо'))
            markup.add(types.KeyboardButton('Изменить блюдо'))
            if message.from_user.username in get_admins(test)['core_admins']:
                markup.add(types.KeyboardButton('Добавить администратора'))
                markup.add(types.KeyboardButton('Удалить администратора'))
            markup.add(types.KeyboardButton('Режим пользователя'))
            bot.reply_to(message, "Добро пожаловать в админ панель. Выберите действие:", reply_markup=markup)
        else:
            bot.reply_to(message, "У вас нет прав(администратора)")

    @bot.message_handler(func=lambda message: message.text in context.admin_commands and message.from_user.username in get_admins(test)['all_admins'])
    def admin(message):
        if message.text == 'Добавить блюдо':

            markup = types.ReplyKeyboardMarkup()
            for i in get_types(test):
                markup.row(types.KeyboardButton(i['type']))

            bot.reply_to(message, "Выберите категорию, в которой будет находиться блюдо:", reply_markup=markup)

            bot.register_next_step_handler(message, add_type)

        if message.text == 'Изменить блюдо':
            bot.reply_to(message, "Функция пока не готова")
            start(message)
        if message.text == "Режим пользователя":
            start(message)

    def add_type(message):
        temp = []
        for i in get_types(test):
            temp.append(i['type'])

        if message.text not in temp:
            markup = types.ReplyKeyboardMarkup()
            for i in get_types(test):
                markup.row(types.KeyboardButton(i['type']))
            bot.reply_to(message, "Произошла ошибка. Выберите категорию используя кнопки", reply_markup=markup)

        dish = dict()
        dish['type'] = message.text
        dish['type_id'] = int([i['id'] for i in get_types(test) if i['type'] == message.text][0])
        bot.reply_to(message, "Отправьте название блюда", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, add_name, dish)

    def add_name(message, dish):
        dish['name'] = message.text
        bot.reply_to(message, "Отправьте ингредиенты блюда")
        bot.register_next_step_handler(message, add_ingredients, dish)

    def add_ingredients(message, dish):
        dish['ingredients'] = message.text
        bot.reply_to(message, "Отправьте рецепт блюда")
        bot.register_next_step_handler(message, add_recipe, dish)

    def add_recipe(message, dish):
        dish['recipe'] = message.text
        bot.reply_to(message, "Отправьте фото блюда")
        bot.register_next_step_handler(message, add_photo, dish)

    def add_photo(message, dish):
        if not message.photo:
            bot.reply_to(message, "Ошибка. Отправьте фото блюда")
            bot.register_next_step_handler(message, add_photo, dish)
        dish['photo_id'] = message.photo[-1].file_id
        dish['add_by'] = message.from_user.username
        add_dish(dish, test)
        bot.reply_to(message, "Новое блюдо добавлено")
        admin(message)

    @bot.message_handler(func=lambda message: message.text in context.core_admin_commands and message.from_user.username in get_admins(test)['core_admins'])
    def core_admin(message):
        if message.text == 'Добавить администратора':
            bot.reply_to(message, "Отправьте ник нового администратора", reply_markup=types.ReplyKeyboardRemove())
            bot.register_next_step_handler(message, add_admin)

        if message.text == 'Удалить администратора':
            bot.reply_to(message, "Функция пока не готова")
            start(message)

    def add_admin(message):
        add_new_admin(message.text, test)
        bot.reply_to(message, "Новый администратор добавлен")
        admin(message)

    @bot.message_handler(func=lambda message: (message.text not in context.admin_commands + context.core_admin_commands) and message.text)
    def error(message):
        start(message)

    bot.polling(non_stop=True, interval=0)
