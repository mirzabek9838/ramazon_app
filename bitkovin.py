import telebot
from telebot import types
from py_currency_converter import convert
from pycoingecko import CoinGeckoAPI
cg = CoinGeckoAPI()

bot = telebot.TeleBot('6447602949:AAH7XJJrFW73P5Y6L6WGXBhkmBIAbacpJRg')


@bot.message_handler(commands=['start'])
def main(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('Курс крипть'), types.KeyboardButton('Курс фиата'), types.KeyboardButton('Конвертер'))
    cr = bot.send_message(message.chat.id, 'Мы на главной', reply_markup=b1)
    bot.register_next_step_handler(cr, step)

def step(message):
    if message.text == 'Курс крипты':
        step2(message)
    elif message.text == 'Курс фиата':
        fiat(message)
    elif message.text == 'Конвертер':
        konv(message)

def konv(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('Bitcoin'), types.KeyboardButton('Ethereum'), types.KeyboardButton('Litecoin'), types.KeyboardButton('Polygon'), types.KeyboardButton('Uniswap'),types.KeyboardButton('Назад'))
    msg = bot.send_message(message.chat.id, 'Выберите криптовалюту', reply_markup=b1)
    bot.register_next_step_handler(msg, konv2)

def konv2(message):
    if message.text == 'Bitcoin':
        msg = bot.send_message(message.chat.id, 'Сколько вы хотите конвертировать ВТС?')
        bot.register_next_step_handler(msg, bbtc)
    elif message.text == 'Ethereum':
        msg = bot.send_message(message.chat.id, 'Сколько вы хотите конвертировать ETH?')
        bot.register_next_step_handler(msg, eeth)
    elif message.text == 'Litecoin':
        msg = bot.send_message(message.chat.id, 'Сколько вы хотите конвертировать LTC?')
        bot.register_next_step_handler(msg, lltc)
    elif message.text == 'Polygon':
        msg = bot.send_message(message.chat.id, 'Сколько вы хотите конвертировать MATIC?')
        bot.register_next_step_handler(msg, mmatic)
    elif message.text == 'Uniswap':
        msg = bot.send_message(message.chat.id, 'Сколько вы хотите конвертировать uni?')
        bot.register_next_step_handler(msg, uuni)
    elif message.text == 'Назад':
        main(message)

def bbtc(message):
    konv2 = message.text
    konv2 = int(konv2)

    price = cg.get_price(ids='bitcoin', vs_currencies='usd')
    bot.send_message(message.chat.id, f'{konv2} BTC == {price["bitcoin"]["usd"] * konv2} $')
    main(message)

def eeth(message):
    konv2 = message.text
    konv2 = int(konv2)

    price = cg.get_price(ids='Ethereum', vs_currencies='usd')
    bot.send_message(message.chat.id, f'{konv2} ETH == {price["ethereum"]["usd"] * konv2} $')
    main(message)

def lltc(message):
    konv2 = message.text
    konv2 = int(konv2)

    price = cg.get_price(ids='Litecoin', vs_currencies='usd')
    bot.send_message(message.chat.id, f'{konv2} LTC == {price["litecoin"]["usd"] * konv2} $')
    main(message)

def mmatic(message):
    konv2 = message.text
    konv2 = int(konv2)

    price = cg.get_price(ids='Polygon', vs_currencies='usd')
    bot.send_message(message.chat.id, f'{konv2} MATIC == {price["matic-network"]["usd"] * konv2} $')
    main(message)

def uuni(message):
    konv2 = message.text
    konv2 = int(konv2)

    price = cg.get_price(ids='Uniswap', vs_currencies='usd')
    bot.send_message(message.chat.id, f'{konv2} uni == {price["uniswap"]["usd"] * konv2} $')
    main(message)

def fiat(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('USD'), types.KeyboardButton('RUB'), types.KeyboardButton('Главная'))
    q = bot.send_message(message.chat.id, 'Курс фиата', reply_markup=b1)
    bot.register_next_step_handler(q, fiat_step2)

def fiat_step2(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('Назад'))
    if message.text == 'USD':
        price = convert(base='USD', amount=1, to=['RUB', 'EUR', 'UAH', 'KZT'])
        bot.send_message(message.chat.id, f'1 USD == {price["RUB"]} RUB\n'
                                        f'1 USD == {price["EUR"]} EUR\n'
                                        f'1 USD == {price["UAH"]} UAH\n'
                                        f'1 USD == {price["KZT"]} KZT')
        go_main = bot.send_message(message.chat.id, 'Вернуться назад', reply_markup=b1)
        bot.register_next_step_handler(go_main, fiat)
    if message.text == 'RUB':
        price = convert(base='RUB', amount=1, to=['USD', 'EUR', 'UAH', 'KZT'])
        bot.send_message(message.chat.id, f'1 RUB == {price["USD"]} USD\n'
                                        f'1 RUB == {price["EUR"]} EUR\n'
                                        f'1 RUB == {price["UAH"]} UAH\n'
                                        f'1 RUB == {price["KZT"]} KZT')
        go_main = bot.send_message(message.chat.id, 'Вернуться назад', reply_markup=b1)
        bot.register_next_step_handler(go_main, fiat)
    if message.text == 'Главная':
        main(message)



def step2(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('Курс и USD'), types.KeyboardButton('Курс и RUB'), types.KeyboardButton('Главная'))
    q = bot.send_message(message.chat.id, 'Курс моих токенов', reply_markup=b1)
    bot.register_next_step_handler(q, step3)

def step3(message):
    b1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    b1.add(types.KeyboardButton('Назад'))
    if message.text == 'Курс и USD':
        price = cg.get_price(ids='bitcoin, ethereum, litecoin, matic-network, uniswap', vs_currencies='usd')
        bot.send_message(message.chat.id, f'Мои токень:\n\n'
                                          f'Bitcoin💰  == {price["bitcoin"]["usd"]}$\n'
                                          f'Ethereum💰 == {price["ethereum"]["usd"]}$\n'
                                          f'Litecoin💰 == {price["litecoin"]["usd"]}$\n'
                                          f'Polygon💰 == {price["matic-network"]["usd"]}$\n'
                                          f'Uniswap💰 == {price["uniswap"]["usd"]}$', reply_markup=b1)
        go_main = bot.send_message(message.chat.id, 'Вернуться назад', reply_markup=b1)
        bot.register_next_step_handler(go_main, step2)

    elif message.text == 'Курс и RUB':
        price = cg.get_price(ids='bitcoin, ethereum, litecoin, matic-network, uniswap', vs_currencies='rub')
        bot.send_message(message.chat.id, f'Мои токень:\n\n'
                                          f'Bitcoin💰  == {price["bitcoin"]["rub"]}P\n'
                                          f'Ethereum💰 == {price["ethereum"]["rub"]}P\n'
                                          f'Litecoin💰 == {price["litecoin"]["rub"]}P\n'
                                          f'Polygon💰 == {price["matic-network"]["rub"]}P\n'
                                          f'Uniswap💰 == {price["uniswap"]["rub"]}', reply_markup=b1)
        go_main = bot.send_message(message.chat.id, 'Вернуться назад', reply_markup=b1)
        bot.register_next_step_handler(go_main, step2)
    elif message.text == 'Главная':
        main(message)



bot.polling()
