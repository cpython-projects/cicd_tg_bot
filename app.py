from flask import Flask, request
from dotenv import load_dotenv
import os
import telebot

load_dotenv('.env')
TOKEN = os.environ.get('TOKEN', '')


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


@bot.callback_query_handler(func=lambda call: True)
def handle_program_callback(call):
    # Отримання посилання на програму зі зворотного виклику
    program_link = call.data

    # Відправка повідомлення з посиланням на програму
    bot.send_message(chat_id=call.message.chat.id, text=f"Ось посилання на програму: {program_link}")



@app.route('/' + TOKEN, methods=['POST'])
def get_message():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '', 200


@app.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://test-bot-cicd-knu.herokuapp.com/' + TOKEN)
    return '', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
