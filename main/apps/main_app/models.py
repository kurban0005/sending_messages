from django.db import models
from ..users_app.models import User

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    email_sent = models.BooleanField(default=False)
    sms_sent = models.BooleanField(default=False)
    telegram_sent = models.BooleanField(default=False)
    date_add = models.DateTimeField(auto_now_add=True)