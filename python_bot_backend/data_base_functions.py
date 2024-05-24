import sqlite3
from datetime import datetime
import json


def get_connection():
    return sqlite3.connect('my_database.db')


class SQLiteUser:
    id = int
    username = str
    phone = int
    orders_count = int

    def __init__(self, user_id: int):
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM Users WHERE id = ?', (user_id,))
            curren_user = cursor.fetchone()
            if curren_user:
                self.id = curren_user[0]
                self.username = curren_user[1]
                self.phone = curren_user[2]
                self.orders_count = curren_user[3]
            else:
                cursor.execute('INSERT INTO Users (id, orders_count) VALUES (?, ?)',
                               (user_id, 0,))
                self.id = user_id
                self.username = None
                self.phone = None
                self.orders_count = 0
                self.date = ''

    def __getattribute__(self, item):
        if item == "username":
            with get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM Users WHERE id = ?', (self.id,))
                curren_user = cursor.fetchone()
                return curren_user[1]
        elif item == "phone_number":
            with get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM Users WHERE id = ?', (self.id,))
                curren_user = cursor.fetchone()
                return curren_user[2]
        elif item == "orders_count":
            with get_connection() as connection:
                cursor = connection.cursor()
                cursor.execute('SELECT * FROM Users WHERE id = ?', (self.id,))
                curren_user = cursor.fetchone()
                return curren_user[4]
        return super().__getattribute__(item)

    def change_username(self, username):
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('UPDATE Users SET username = ? WHERE id = ?', (username, self.id))

    def change_phone(self, phone):
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('UPDATE Users SET phone_number = ? WHERE id = ?', (phone, self.id))

    def change_order_status(self, order_number, new_status):
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('UPDATE OrderDetails SET status = ? WHERE order_id = ?',
                           (new_status, f'{self.id}_{order_number}'))

    def insert_order_data(self, data, status):
        order_id = f"{self.id}_{self.orders_count}"
        with get_connection() as conn:
            c = conn.cursor()
            for item in data['cart']:
                c.execute('''
                    INSERT INTO OrderDetails (order_id, dish_name, quantity, price, status, date)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (order_id, item['name'], item['quantity'], item['price'], status,
                      datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    def increase_orders_count(self):
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('UPDATE Users SET orders_count = orders_count + 1 WHERE id = ?', (self.id,))

    def get_last_order(self):
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM OrderDetails WHERE order_id = ?', (f'{self.id}_{self.orders_count}',))
            curren_user = cursor.fetchall()
            return curren_user

    def get_all_orders(self):
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM OrderDetails WHERE order_id LIKE ?", ('%' + str(self.id) + '%',))
            curren_user = cursor.fetchall()
            return curren_user
    def get_order_with_id(self, order_id):
        with get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM OrderDetails WHERE order_id = ?', (order_id,))
            curren_user = cursor.fetchall()
            return curren_user
