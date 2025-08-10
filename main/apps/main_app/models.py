from django.db import models
from ..users_app.models import User


class Notification(models.Model):
    """
    Класс УВЕДОМЛЕНИЕ.
    Состоит из: пользователя получателя, сообщения,
    статусов отправки: емейл, смс и телеграм,
    и даты добавления.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    email_sent = models.BooleanField(default=False)  # статус отправки емейл
    sms_sent = models.BooleanField(default=False)  # статус отправки смс
    telegram_sent = models.BooleanField(default=False)  # статус отправки телеграм
    date_add = models.DateTimeField(auto_now_add=True)
