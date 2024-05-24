import time

import telebot
from telebot import types
import os
import sys
from requests import ReadTimeout
import config
import data_base_functions

bot = telebot.TeleBot(config.token())
bot.parse_mode = 'html'


@bot.message_handler(commands=['start'])
def welcome(message):
    user = data_base_functions.SQLiteUser(message.chat.id)
    bot.send_message(user.id, config.start_text(), disable_web_page_preview=True, reply_markup=config.start_markup())


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.text == "Наш адрес 📍":
        bot.send_location(message.chat.id, config.latitude, config.longitude)
        bot.send_message(message.chat.id,
                         f"""Наш ресторан расположен по адресу:\n<b><a href="{config.address_link}">Москва, 1-й 
                         Красногвардейский проезд, 22с2</a></b>""",
                         disable_web_page_preview=True)
    elif message.text == "Личный кабинет 🌝":
        user = data_base_functions.SQLiteUser(message.chat.id)
        if user.phone is None:
            bot.send_message(message.chat.id,
                             "Кажется, вы у нас <b>впервые</b> 😱.\nЗарегистрируйтесь, нажав на <b>кнопку ниже</b> 👇.",
                             reply_markup=config.registration_markup())
        else:
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(types.InlineKeyboardButton('📒 Список заказов', callback_data="order_list"))
            bot.send_message(message.chat.id,
                             f"Здравствуйте, <b>{message.from_user.first_name}</b>.\nТелефон для связи: +{user.phone}",
                             reply_markup=markup)


@bot.message_handler(content_types=['contact'])
def contact_received(message):
    contact = message.contact
    user = data_base_functions.SQLiteUser(message.chat.id)
    user.change_username(message.from_user.username)
    user.change_phone(message.contact.phone_number)
    bot.send_message(message.chat.id,
                     f"Приятно познакомится, <b>{contact.first_name}</b>!", reply_markup=config.start_markup())


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "order_list":
            user = data_base_functions.SQLiteUser(call.message.chat.id)
            if user.orders_count == 0:
                bot.send_message(call.message.chat.id,
                                 "Пока у <b>Вас</b> не было заказов. С нетерпением ждём <b>Ваш</b> первый заказ 🥡!")
            else:
                orders_data = user.get_all_orders()
                orders_id_set = set()
                markup = types.InlineKeyboardMarkup(row_width=1)
                for order in orders_data:
                    if order[0] not in orders_id_set:
                        orders_id_set.add(order[0])
                        markup.add(types.InlineKeyboardButton(order[5], callback_data=f'order_list_{order[0]}'))
                bot.send_message(call.message.chat.id, 'Ваша история заказов:', reply_markup=markup)
        elif call.data == "order_processing":
            user = data_base_functions.SQLiteUser(call.message.chat.id)
            order_data = user.get_last_order()
            if order_data[0][4] == 'in progress':
                msg = bot.send_message(call.message.chat.id,
                                       "Отлично! Теперь пришлите, пожалуйста, адрес доставки.\nНам нужны:\n<b>Улица, "
                                       "номер дома, подъезд, этаж</b>.\nЕсли нужно, можете оставить комментарий "
                                       "курьеру.")
                bot.register_next_step_handler(msg, address_final)
            else:
                bot.send_message(call.message.chat.id,
                                 "Извините, что-то пошло не так. "
                                 "Попробуйте сделать заказ ещё раз или напишите в нашу поддержку.")
        elif 'order_in_progress_' in call.data:
            user = data_base_functions.SQLiteUser(call.data.split('_')[3])
            user.change_order_status(user.orders_count, 'cooking')
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("Отдать заказ курьеру", callback_data=f'order_courier_search_{user.id}'))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=call.message.text, reply_markup=markup)
            bot.send_message(user.id, 'Ваш заказ готовится 🍳')
            time.sleep(1)
            bot.send_sticker(user.id, 'CAACAgIAAxkBAAEMJKNmSNZGl599H5bBKDzSFTldS3WrlwAC3wADMNSdERFtkOglJud9NQQ')
        elif 'order_courier_search_' in call.data:
            user = data_base_functions.SQLiteUser(call.data.split('_')[3])
            user.change_order_status(user.orders_count, 'delivery')
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("Заказ доставлен", callback_data=f'order_close_{user.id}'))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=call.message.text, reply_markup=markup)
            bot.send_message(user.id, 'Курьер везёт ваш заказ 🏎')
            time.sleep(1)
            bot.send_sticker(user.id, 'CAACAgIAAxkBAAEMJLFmSOHRuALrWUrYfpz4Ca_qjIEadgACMgEAAqtXxAvSDaRAN23ITDUE')
        elif 'order_close_' in call.data:
            user = data_base_functions.SQLiteUser(call.data.split('_')[2])
            user.change_order_status(user.orders_count, 'closed')
            markup = types.InlineKeyboardMarkup(row_width=1)
            markup.add(
                types.InlineKeyboardButton("Заказ закрыт ✅", callback_data=f'order_close_{user.id}'))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=call.message.text, reply_markup=markup)
            # bot.send_message(user.id, '')
            # time.sleep(1)
            # bot.send_sticker(user.id, 'CAACAgIAAxkBAAEMJLFmSOHRuALrWUrYfpz4Ca_qjIEadgACMgEAAqtXxAvSDaRAN23ITDUE')
        elif 'order_list_' in call.data:
            bot.send_message(call.message.chat.id,
                             config.configurate_order_list_text(call.message.chat.id,
                                                                f'{call.message.chat.id}_{call.data.split("_")[3]}'))


def address_final(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("Заказ взят в работу", callback_data=f'order_in_progress_{message.chat.id}'))
    bot.forward_message(config.restaurant_administration_chat_id, message.chat.id, message.message_id)
    bot.send_message(config.restaurant_administration_chat_id, config.configurate_order_text(message.chat.id,
                                                                                             message.text),
                     reply_markup=markup)
    bot.send_message(message.chat.id, "Получили ваш заказ, вот-вот начнём готовить ❤️")
    time.sleep(1)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEMJg1mSjeLT5weUsjTgLdk5mwLe73vrgACoxUAAv0yWUgg57QVu83WOTUE')


if __name__ == '__main__':
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except (ConnectionError, ReadTimeout) as e:
        sys.stdout.flush()
        os.execv(sys.argv[0], sys.argv)
    else:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
