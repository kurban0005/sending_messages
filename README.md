# Структура:

### Приложения (apps):
1. main_app:
   - Основное приложения для рассылки смс, почты и телеграма.
2. users_app:
   - Приложение для управления пользователями.

### Makefile.
Для быстрого запуска команд. Находится в корневой папке.
### Бот.
Расположение: `main/apps/main_app/management/commands/run_bot.py`
### Уведомления.
Расположение: `main/apps/main_app/notifications.py`
### Дополнительно для удобства:
- отключена валидация пароля регистрации пользователя.
- добавлена кнопка "стать суперпользователем"


# Запуск:
1. Создать виртуальное окружение с помощью `python -m venv name_venv`
2. Активировать его
3. установить все модули `pip freeze > requirements.txt`
4. создайте файл .env (переменные окружения и укажите свои данные там):
   - TELEGRAM_BOT_TOKEN="токен_ТГ_бота"
   - TELEGRAM_BOT_NAME="имя_бота"
   - EMAIL_HOST_USER:"почтаt@mail.com"
   - EMAIL_HOST_PASSWORD:"пароль от почты"
   - TWILIO_PHONE_NUMBER:'your_twilio_phone_number'
   - TWILIO_ACCOUNT_SID:'your_twilio_account_sid'
   - TWILIO_AUTH_TOKEN:'your_twilio_auth_token'
5. Вручную или командой `make bot` запустить бота
6. Вручную или командой `make run` запустить сервер
7. Зайти на сайт `http://127.0.0.1:8000/`
8. Авторизоваться через телеграм, ввести свои данные при необходимости, и нажать на рассылку.
