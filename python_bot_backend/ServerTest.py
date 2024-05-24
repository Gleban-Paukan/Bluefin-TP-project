from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import telebot
import config
import data_base_functions
import json

bot = telebot.TeleBot(config.token())
bot.parse_mode = 'html'
app = Flask(__name__)
CORS(app)


@app.route('/make_order', methods=['POST'])
@cross_origin()
def make_order():
    data = request.json
    user_id = data['telegramUserId']
    print("Получен заказ:", data)
    user = data_base_functions.SQLiteUser(user_id)
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(telebot.types.InlineKeyboardButton(callback_data=f'order_processing', text='Да, всё верно! ✅'))
    user.increase_orders_count()
    user.insert_order_data(data, 'in progress')
    message_data = "".join(
        [f'<b>{item["name"]}</b> — {item["quantity"]} шт. (<i>{item["quantity"] * item["price"]} руб.</i>)\n' for item
         in data['cart']])

    bot.send_message(497365721, f'Ваш заказ:\n{message_data}', reply_markup=markup)
    return jsonify({"success": True})


if __name__ == '__main__':
    app.run(debug=True)
