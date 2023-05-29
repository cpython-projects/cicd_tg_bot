from flask import Flask
from dotenv import load_dotenv
import os
import telebot

load_dotenv('.env')
TOKEN = os.environ.get('TOKEN')

app = Flask(__name__)
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)

@bot.message_handler(commands=['programs'])
def handle_programs(message, filepath=os.path.join('data', 'programs.txt')):

    programs = {}
    with open(filepath, encoding='utf-8') as file:
        for line in file:
            program, link = line.split(';')
            programs[program.strip()] = link.strip()

    # Створення клавіатури з кнопками програм
    keyboard = telebot.types.InlineKeyboardMarkup(row_width=1)
    for program, link in programs.items():
        button = telebot.types.InlineKeyboardButton(text=program, callback_data=link)
        keyboard.add(button)

    # Відправка повідомлення з клавіатурою користувачеві
    bot.send_message(chat_id=message.chat.id, text="Оберіть програму:", reply_markup=keyboard)


if __name__ == '__main__':
    bot.polling()
