import pytest
from telebot import types
from app import handle_programs  # Import the function you want to test


class MockBot:
    def __init__(self):
        self.sent_messages = []

    def send_message(self, chat_id, text, reply_markup=None):
        self.sent_messages.append((chat_id, text, reply_markup))


def test_handle_programs(prepare_text_file, monkeypatch):
    bot = MockBot()
    monkeypatch.setattr('app.bot', bot)
    user = types.User(id=123, is_bot=False, first_name="John")
    chat = types.Chat(id=456, type="private")

    message = types.Message(
        message_id=123,
        from_user=user,
        date=None,
        chat=chat,
        content_type=None,
        options={},
        json_string=None
    )

    handle_programs(message, prepare_text_file)

    # Check that one message was sent
    assert len(bot.sent_messages) == 1

    # Check the content of the sent message
    chat_id, text, reply_markup = bot.sent_messages[0]
    assert chat_id == message.chat.id  # Check the chat ID
    assert text == "Оберіть програму:"  # Check the message text

    # Check the keyboard buttons
    expected_programs = {}
    with open(prepare_text_file, encoding='utf-8') as file:
        for line in file:
            program, link = line.split(';')
            expected_programs[program.strip()] = link.strip()

    assert len(reply_markup.keyboard) == len(expected_programs)

    for row, expected_row in zip(reply_markup.keyboard, expected_programs.items()):
        program, link = expected_row
        button = row[0]
        assert button.text == program
        assert button.callback_data == link
