from django.core.management.base import BaseCommand
from dotenv import load_dotenv, find_dotenv
from ....users_app.models import User
import telebot
import os

load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.getenv('TELEGRAM_BOT_TOKEN'))


class Command(BaseCommand):
    ''' ЗАПУСК БОТА через infinity_polling. '''
    help = 'Run your Telegram-bot'

    def handle(self, *args, **options):
        print('БОТ запущен.')
        bot.infinity_polling()  # запуск бота
        print('БОТ выключен.')


@bot.message_handler(commands=['start'])
def start(message):
    ''' АВТОРИЗАЦИЯ ЧЕРЕЗ ТЕЛЕГРАМ БОТа. '''
    telegram_id = message.chat.id
    token = message.text.split()[1] if len(message.text.split()) > 1 else None
    if token is not None:
        try:
            user = User.objects.update_or_create(telegram_id=telegram_id, defaults={
                'username': message.from_user.username,
                'token': token, })
            markup = telebot.types.InlineKeyboardMarkup()
            markup.add(telebot.types.InlineKeyboardButton("перейти на сайт",
                                                          url=f'http://{os.getenv("DOMAIN")}/users_app/login/'))
            bot.send_message(message.chat.id, f"Вход выполнен успешно", reply_markup=markup)
        except Exception as e:
            print(f'Ошибка при обработке сообщения: {e}')
            bot.send_message(chat_id=telegram_id,
                             text="Произошла ошибка при попытке входа. Попробуйте еще раз.")
    else:
        bot.send_message(chat_id=telegram_id,
                         text="Для того, что-бы войти в аккаунт перейдите по ссылке на сайте")
