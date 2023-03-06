# подключение библиотек
import json
from secrets import token_urlsafe

from telebot import TeleBot, types

from collections import OrderedDict
from faker import Faker
locales = OrderedDict([
    ('en_US', 1),
    ('ru_RU', 2),
    ('en_GB', 3),
    ('pt_BR', 4),
])
fake = Faker(locales)


# TODO: вставить свой токен
TOKEN = 'вставить_свой_токен'
bot = TeleBot(TOKEN, parse_mode='html')

# объект клавиаутры
main_menu_reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
# первый ряд кнопок
main_menu_reply_markup.row(
    types.KeyboardButton(text="EN 🇺🇸"), types.KeyboardButton(text="RU 🇷🇺")
)
# второй ряд кнопок
main_menu_reply_markup.row(
    types.KeyboardButton(text="EN 🇬🇧"), types.KeyboardButton(text="PT 🇧🇷")
)

# обработчик команды '/start'
@bot.message_handler(commands=['start'])
def start_message_handler(message: types.Message):
    # отправляем ответ на команду '/start'
    # прикрепляем объект клавиатуры к сообщению
    bot.send_message(
        chat_id=message.chat.id,
        text="Hi! I will help you to generate fake data for test users in several languages. "\
        "Select language and country 👇🏻",
        reply_markup=main_menu_reply_markup
    )

# обработчик всех остальных сообщений
@bot.message_handler()
def message_handler(message: types.Message):
    # определяем страну
    # или отправляем ошибку
    if message.text == 'EN 🇺🇸':
        country = 'en_US'
    elif message.text == 'RU 🇷🇺':
        country = 'ru_RU'
    elif message.text == 'EN 🇬🇧':
        country = 'en_GB'
    elif message.text == 'PT 🇧🇷':
        country = 'pt_BR'
    else:
        # если текст не совпал ни с одной из кнопок 
        # выводим ошибку
        bot.send_message(
            chat_id=message.chat.id,
            text='I dont understand this :(',
        )
        return

    person = {}
    person['name'] = fake[country].name()
    person['email'] = fake.email()
    person['address'] = fake[country].address()
    person['password'] = token_urlsafe(10)

    # и выводим пользователю
    bot.send_message(
        chat_id=message.chat.id,
        text=f"Here is your fake data for {message.text}:\n<code>"\
        f"{person}</code>"
    )
    bot.send_message(
        chat_id=message.chat.id,
        text="For more data select language and country 👇🏻",
        reply_markup=main_menu_reply_markup
    )


# главная функция программы
def main():
    # запускаем нашего бота
    bot.infinity_polling()


if __name__ == '__main__':
    main()
