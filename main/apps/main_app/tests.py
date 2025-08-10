from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from unittest.mock import patch

User = get_user_model()


class MainAppViewsTestCase(TestCase):
    """
    Тесты для проверки поведения представлений (views) главного приложения.

    Включает тестирование следующих сценариев:
    - Проверка доступа к главной странице (index) для неаутентифицированных пользователей
    - Проверка вызова функций уведомлений (email, sms, telegram)
    """

    def setUp(self):
        """
        Выполняется перед каждым тестом.
        Создаем клиент и тестового пользователя.
        """
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_index_requires_login(self):
        """
        Проверка, что доступ к главной странице (index) требует аутентификации.
        Неаутентифицированный пользователь перенаправляется на страницу логина.
        """
        url = reverse('main_app:index')
        response = self.client.get(url)
        self.assertRedirects(response, f"{reverse('users_app:login')}?next={url}")

        # Логинимся и проверяем доступ к странице
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main_app/index.html')

    @patch('apps.main_app.views.send_all_notification')
    def test_notify_user_calls_send_all_notification(self, mock_send):
        """
        Проверка, что при обращении к представлению отправки уведомлений
        вызывается функция send_all_notification с правильными параметрами.
        """
        self.client.login(username='testuser', password='testpassword')
        url = reverse('main_app:send_notification')
        self.client.get(url)
        mock_send.assert_called_once_with(self.user, "This is a test notification!")

    @patch('apps.main_app.views.send_sms_notification')
    def test_sms_notification_calls_send_sms_notification(self, mock_send):
        """
        Проверка, что при обращении к представлению отправки SMS
        вызывается функция send_sms_notification с правильными параметрами.
        """
        self.client.login(username='testuser', password='testpassword')
        url = reverse('main_app:send_sms')
        self.client.get(url)
        mock_send.assert_called_once_with(self.user, "Это тестовое сообщение написано специально для вас!")

    @patch('apps.main_app.views.send_email_notification')
    def test_email_notification_calls_send_email_notification(self, mock_send):
        """
        Проверка, что при обращении к представлению отправки email
        вызывается функция send_email_notification с правильными параметрами.
        """
        self.client.login(username='testuser', password='testpassword')
        url = reverse('main_app:send_email')
        self.client.get(url)
        mock_send.assert_called_once_with(self.user, "Это тестовое сообщение написано специально для вас!")

    @patch('apps.main_app.views.send_telegram_notification')
    def test_telegram_notification_calls_send_telegram_notification(self, mock_send):
        """
        Проверка, что при обращении к представлению отправки Telegram-уведомления
        вызывается функция send_telegram_notification с правильными параметрами.
        """
        self.client.login(username='testuser', password='testpassword')
        url = reverse('main_app:send_tg')
        self.client.get(url)
        mock_send.assert_called_once_with(self.user, "Это тестовое сообщение написано специально для вас!")
