from django.core.mail import send_mail
from twilio.rest import Client as TwilioClient
from .management.commands.run_bot import bot
from .models import Notification
from dotenv import load_dotenv
import os
from loguru import logger

load_dotenv()


def send_all_notification(user, message):
    '''Отправка уведомления: EMAIL, SMS, TELEGRAM. '''
    # Создаем уведомление
    notification = Notification.objects.create(user=user, message=message)  # Создаем уведомление
    try:  # Попробовать отправить на Email
        send_mail(
            subject='Notification',
            message=message,
            from_email=None,
            recipient_list=[user.email],
        )
        notification.email_sent = True  # смена статуса отправки
        notification.save()
    except Exception as e:
        logger.error(f'\nНЕ ПОЛУЧИЛОСЬ ОТПРАВИТЬ EMAIL: {e}.')

    try:  # Попробовать отправить по SMS
        load_dotenv()
        twilio_client = TwilioClient(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
        twilio_client.messages.create(
            body=message,
            from_=os.getenv('TWILIO_PHONE_NUMBER'),
            to=user.phone_number, )
        notification.sms_sent = True  # смена статуса отправки
        notification.save()
    except Exception as e:
        logger.error(f'\nНЕ ПОЛУЧИЛОСЬ ОТПРАВИТЬ СМС: {e}')

    try:  # Попробовать отправить в Telegram
        bot.send_message(chat_id=user.telegram_id, text=message)
        notification.telegram_sent = True  # смена статуса отправки
        notification.save()
        return
    except Exception as e:
        logger.error(f'\nНЕ ПОЛУЧИЛОСЬ ОТПРАВИТЬ СООБЩЕНИЕ В ТЕЛЕГРАМ: {e}')


def send_sms_notification(user, message):
    '''Отправка уведомления по СМС. '''
    notification = Notification.objects.create(user=user, message=message)  # Создаем уведомление
    try:
        load_dotenv()
        twilio_client = TwilioClient(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))
        twilio_client.messages.create(
            body=message,
            from_=os.getenv('TWILIO_PHONE_NUMBER'),
            to=user.phone_number, )
        notification.sms_sent = True  # смена статуса отправки
        notification.save()
        return
    except Exception as e:
        logger.error(f'\nОШИБКА. НЕ ПОЛУЧИЛОСЬ ОТПРАВИТЬ СМС: {e}')


def send_email_notification(user, message):
    '''Отправка уведомления на EMAIL. '''
    notification = Notification.objects.create(user=user, message=message)
    try:
        if user.email:
            send_mail(
                subject='Notification',
                message=message,
                from_email=None,
                recipient_list=[user.email], )
            notification.email_sent = True  # смена статуса отправки
            notification.save()
            return
        else:
            logger.error(f'\nУКАЖИТЕ СВОЙ EMAIL')
    except Exception as e:
        logger.error(f'\nНЕ ПОЛУЧИЛОСЬ ОТПРАВИТЬ EMAIL: {e}')


def send_telegram_notification(user, message):
    '''Отправка уведомления в TELEGRAM. '''
    notification = Notification.objects.create(user=user, message=message)  # Создаем уведомление
    try:
        bot.send_message(chat_id=user.telegram_id, text=message)
        notification.telegram_sent = True  # смена статуса отправки
        notification.save()
        return
    except Exception as e:
        logger.error(f'\nСООБЩЕНИЕ В ТЕЛЕГРАМ НЕ ДОСТАВЛЕНО: {e}')
