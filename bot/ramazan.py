import telebot
import requests
import json
import webbrowser
from telebot import types
import sqlite3

bot = telebot.TeleBot('6067944978:AAHC7N3_Atfju7Ffeomdqqz21fP89GL5qdE')
API = 'c2e1710e6b1b47de9290b3d4270e8c67'
name = None


@bot.message_handler(commands=['pogoda'])
def main(message):
    bot.send_message(message.chat.id, 'Привет рад тебя видеть! Напиши название городь')


@bot.message_handler(content_types=['text'])
def get_weather(message):
    city = message.text.strip().lower()
    res = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API}&units=metric')
    if res.status_code == 200:
        data = json.loads(res.text)
        temp = data["main"]["temp"]
        bot.reply_to(message, f'Сечас погода: {temp}')

        image = 'image3.png' if temp > 5.0 else 'image4.png'
        file = open('./' + image, 'rb')
        bot.send_photo(message.chat.id, file)
    else:
        bot.reply_to(message, f'Город указан не верно')


@bot.message_handler(commands=['sart'])
def main(message):
    conn = sqlite3.connect('google.sql')
    cur = conn.cursor()

    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), pass varchar(50))')
    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Привет сейчас тебя зарегистрируем! Введите ваше имя')
    bot.register_next_step_handler(message, user_name)


def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'Введите пароль')
    bot.register_next_step_handler(message, user_pass)


def user_pass(message):
    password = message.text.strip()

    conn = sqlite3.connect('google.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, pass) VALUES ('%s', '%s' )" % (name, password))
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Список ползователей', callback_data='users'))
    bot.send_message(message.chat.id, 'Пользователь зарегистирирован!', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    conn = sqlite3.connect('google.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    info = ''
    for el in users:
        info += f'Имя: {el[1]}, пароль: {el[2]}\n'

    cur.close()
    conn.close()

    bot.send_message(call.message.chat.id, info)


@bot.message_handler(commands=['smart'])
def smart(message):
    markup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('Last name First name')
    markup.row(btn1)
    btn2 = types.KeyboardButton('ID')
    btn3 = types.KeyboardButton('Language')
    markup.row(btn2, btn3)
    file = open('./images.jpeg', 'rb')
    bot.send_photo(message.chat.id, file, reply_markup=markup)
    bot.send_message(message.chat.id, 'Hello', reply_markup=markup)
    bot.register_next_step_handler(message, on_click)


def on_click(message):
    if message.text == 'Last name First name':
        bot.send_message(message.chat.id, f'{message.from_user.first_name} {message.from_user.last_name}')
    if message.text == 'ID':
        bot.send_message(message.chat.id, f'{message.from_user.id}')
    elif message.text == 'Language':
        bot.send_message(message.chat.id, f'{message.from_user.language_code }')


@bot.message_handler(commands=['site', 'website'])
def site(message):
    webbrowser.open('https:/google.com')


@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(message.chat.id, f'Привет!, {message.from_user.first_name} {message.from_user.last_name}')


@bot.message_handler()
def info(message):
    if message.text.lower() == 'mirza':
        bot.send_message(message.chat.id, f'<b>Привет Mirza !!!!</b>', parse_mode='html')
    if message.text.lower() == 'id':
        bot.send_message(message.chat.id, f'ID {message.from_user.id}')
    elif message.text.lower() == 'language':
        bot.reply_to(message, f' Язык , {message.from_user.language_code }')


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Перейти на сайт', url='https://google.com')
    markup.row(btn1)
    btn2 = types.InlineKeyboardButton('Удалить фото', callback_data='delete')
    btn3 = types.InlineKeyboardButton('Изменить текст', callback_data='edit')
    markup.row(btn2, btn3)
    bot.reply_to(message, 'Какое красивое фото!', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text', callback.message.chat.id, callback.message.message_id)





bot.polling(none_stop=True)



