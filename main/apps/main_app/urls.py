from django.urls import path
from . import views

app_name = 'main_app'
urlpatterns = [
    path('', views.index, name='index'),
    path('send_notification', views.notify_user, name='send_notification'), # отправка всех уведомлений СМС+Емейл+ТГ
    path('send_email', views.email_notification, name='send_email'),    # отправка уведомлений Email
    path('send_tg', views.telegram_notification, name='send_tg'),   # отправка уведомлений Телеграм
    path('send_sms', views.sms_notification, name='send_sms'),# отправка уведомлений СМС
]
