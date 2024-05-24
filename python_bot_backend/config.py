from telebot import types
import data_base_functions

address_link = 'https://yandex.ru/maps/213/moscow/house/1_y_krasnogvardeyskiy_proyezd_22s2/Z04YcwRlSkUCQFtvfXt0cHlrYA' \
               '==/?ll=37.536582%2C55.750892&z=18.6'
latitude = 55.751584
longitude = 37.535305

gleb_admin = 1125076741
courier_chat_id = -4166109346
restaurant_administration_chat_id = -4190623902

order_statuses = {
    'in progress': 'Создан ✅',
    'cooking': 'Готовим 🧑🏼‍🍳',
    'delivery': 'Доставляется 🏃🏽',
    'closed': 'Доставлен ✅',
    'canceled': 'Отменен ❌'
}


def registration_markup():
    registration_markup_ = types.ReplyKeyboardMarkup(resize_keyboard=True)
    registration_markup_.add(types.KeyboardButton("Зарегистрироваться ☎️", request_contact=True))
    return registration_markup_


def start_markup():
    start_markup_ = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_markup_.add(types.KeyboardButton("Наш адрес 📍"), types.KeyboardButton("Личный кабинет 🌝"))
    # start_markup_.add(types.KeyboardButton("Меню 📖", web_app=types.WebAppInfo(
    #     "https://gleban-paukan.github.io/Second_python_project/")))
    return start_markup_


def token():
    token_ = "7093458414:AAFWD3zjJD87bUUAMKsBbd9U8k-JbY_57L8"
    return token_


def start_text():
    start_text_ = """<b><a href = "https://bluefin.moscow">BLUEFIN</a></b> - первая океаническая доставка по 
    <b>Москве и Московской области</b>: премиальные роллы 🍣, эксклюзивная рыба и морепродукты 🐡, свежайшие поставки 
    устриц и ежей 🍥, которые доставляются на льду прямо к вашему столу.

    Еженедельно мы привозим высочайшего качества рыбу с морских и океанических берегов<b> Японии, Шри-Ланки, 
    Дальнего Востока, Мурманска 🛫. </b>

    С 2018 года команда <b><a href = "https://bluefin.moscow">BLUEFIN</a></b> удивляет свою аудиторию высочайшим 
    качеством продукции, продуманной упаковкой, уникальной сервировкой и заботливым сервисом 🍽. Этот бот создан в 
    качестве аналога нашего сайта, тут вы сможете посмотреть наше меню и заказать доставку 🥡."""
    return start_text_


def configurate_order_text(user_id: int, address: str) -> str:
    user = data_base_functions.SQLiteUser(user_id)
    order_data = user.get_last_order()
    print(order_data)
    order_text = "".join(
        [f'<b>{item[1]}</b> — {item[2]} шт. (<i>{item[2] * item[3]} руб.</i>)\n' for item
         in order_data]) + f'\n\n<b>Итоговая сумма заказа' \
                           f'</b>:\n {sum([item[2] * item[3] for item in order_data])}\n\nАдрес заказа: {address}'
    return order_text


def configurate_order_list_text(user_id: int, order_id: str) -> str:
    user = data_base_functions.SQLiteUser(user_id)
    order_data = user.get_order_with_id(order_id)
    message_data = "".join([f'<b>{item[1]}</b> — {item[2]} шт. (<i>{item[2] * item[3]} руб.</i>)\n    '
                            for item in order_data])
    text = f'''
<b>Дата заказа: </b>{order_data[0][5]}

<b>Состав заказа:</b>
    {message_data}

<b>Статус заказа:</b> {order_statuses[order_data[0][4]]}
    '''
    return text
