import telebot
from telebot import types
import sqlite3

bot = telebot.TeleBot(token='8590419562:AAEI95E6vVVYKxi84KgILo7aL05NqUkrejw')
name = None
surname = None

@bot.message_handler(commands=['start'])
def send_welcome(message):
    conn = sqlite3.connect('Telegrambase.sql')
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name varchar(50), surname varchar(50))''')
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Привет, сейчас тебя зарегестрируем! Введите своё имя')
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите Фамилию')
    bot.register_next_step_handler(message, user_surname)

def user_surname(message):
    global surname
    surname = message.text.strip()
    conn = sqlite3.connect('Telegrambase.sql')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, surname) VALUES ('%s', '%s')" % (name, surname))
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован!', reply_markup=markup)


markup = types.InlineKeyboardMarkup()
bt1 = types.InlineKeyboardButton('Перейти на сайт', url='https://google.com') # Кномпка на переход сайт нашего проекта
markup.row(bt1)
bt2 = types.InlineKeyboardButton('Помощь', callback_data ='help')
bt3 = types.InlineKeyboardButton('Мои занятия', callback_data ='myfitness')
markup.row(bt3, bt2)
bt4 = types.InlineKeyboardButton('Мой профиль', callback_data ='info')
markup.row(bt4)

@bot.callback_query_handler(func=lambda call: call.data == 'help')
def callback_message(call):
    bot.send_message(call.message.chat.id, 'Чтобы посмотреть все свои занятия нужно нажать на кнопку "Мои занятия"', reply_markup=markup)
@bot.callback_query_handler(func=lambda call: call.data == 'myfitness')
def callback_message(call):
    bot.send_message(call.from_user.id, 'Твои занятия: ', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'info')
def callback_message(call):
    conn = sqlite3.connect('Telegrambase.sql')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users ORDER BY id DESC LIMIT 1")
    users = cur.fetchall()
    info = ''
    for i in users:
        info += f'Мой профиль: \nИмя: {i[1]}, Фамилия: {i[2]} \nТвои занятия:'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info, reply_markup=markup)


bot.polling(none_stop=True)