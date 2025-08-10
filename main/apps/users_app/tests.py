from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewsTestCase(TestCase):
    """
    Тесты для проверки поведения представлений (views) приложения пользователей.

    Включает тестирование следующих сценариев:
    - Авторизация (login): успешная, с неверными данными, проверка контекста
    - Выход из системы (logout)
    - Регистрация (register): успешная и с ошибками в данных
    - Редактирование профиля пользователя (edit_user)
    - Просмотр личного кабинета (my_account)
    - Проверка и изменение флагов суперпользователя (user_is_superuser)
    """

    @classmethod
    def setUpTestData(cls):
        """
        Создание неизменяемых данных для всех тестов класса.
        Выполняется один раз для оптимизации.
        """
        cls.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            email='test@example.com'
        )

    def setUp(self):
        """
        Выполняется перед каждым тестом.
        Создаем клиент для имитации запросов.
        """
        self.client = Client()

    # --- Login View Tests ---

    def test_login_view_redirects_authenticated_user(self):
        """
        Проверка, что аутентифицированный пользователь при обращении к login view
        перенаправляется на главную страницу (index).
        """
        logged_in = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(logged_in, "Не удалось залогиниться с корректными данными")

        response = self.client.get(reverse('users_app:login'))
        self.assertRedirects(response, reverse('main_app:index'))

    def test_login_view_invalid_credentials_shows_error(self):
        """
        Проверка, что при вводе неверных учетных данных
        отображается страница логина с ошибкой.
        """
        response = self.client.post(reverse('users_app:login'), {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users_app/login.html')
        self.assertIn('error', response.context)
        self.assertTrue(response.context['error'], "Ошибка не отображается при неверных данных")

    def test_login_view_contains_telegram_context(self):
        """
        Проверка, что контекст страницы login содержит переменную TELEGRAM_BOT_NAME.
        Используется для интеграции с Telegram-ботом.
        """
        response = self.client.get(reverse('users_app:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users_app/login.html')
        self.assertIn('TELEGRAM_BOT_NAME', response.context)

    # --- Logout View Tests ---

    def test_logout_view_logs_out_user(self):
        """
        Проверка, что logout view корректно завершает сессию пользователя.
        После выхода пользователь не должен быть аутентифицирован.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('users_app:logout'))

        self.assertEqual(response.status_code, 200)
        self.assertNotIn('_auth_user_id', self.client.session, "Пользователь остался в сессии после logout")

    # --- Register View Tests ---

    def test_register_view_creates_user_on_valid_data(self):
        """
        Проверка успешной регистрации нового пользователя с валидными данными.
        После регистрации происходит редирект на главную страницу.
        """
        response = self.client.post(reverse('users_app:register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'email': 'new@example.com'
        })

        self.assertRedirects(response, reverse('main_app:index'))
        self.assertTrue(User.objects.filter(username='newuser').exists(), "Пользователь не создан")

    def test_register_view_shows_error_on_invalid_data(self):
        """
        Проверка, что при неверных данных регистрации (несовпадение паролей, некорректный email)
        отображается страница регистрации с ошибками.
        """
        response = self.client.post(reverse('users_app:register'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'differentpassword',
            'email': 'invalid-email'
        })

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users_app/register.html')
        self.assertIn('error', response.context)
        self.assertTrue(response.context['error'], "Ошибка не отображается при неверных данных регистрации")

    # --- Edit User View Tests ---

    def test_edit_user_view_get_authenticated(self):
        """
        Проверка, что авторизованный пользователь может получить страницу редактирования профиля.
        Проверяется корректность шаблона и контекста.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('users_app:edit_user'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users_app/edit_user.html')
        self.assertEqual(response.context['user'], self.user)

    def test_edit_user_view_post_updates_user(self):
        """
        Проверка, что POST-запрос на редактирование профиля корректно обновляет данные пользователя
        и происходит редирект на главную страницу.
        """
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(reverse('users_app:edit_user'), {
            'username': 'updateduser',
            'email': 'updated@example.com',
            'phone_number': '+79990000000',
            'number': '+79990000000',
        })

        self.assertRedirects(response, reverse('main_app:index'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.email, 'updated@example.com')

    # --- My Account View Tests ---

    def test_my_account_view_authenticated(self):
        """
        Проверка, что авторизованный пользователь может получить страницу личного кабинета.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('users_app:my_account'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users_app/my_account.html')

    # --- User is Superuser Tests ---

    def test_user_is_not_superuser_by_default(self):
        """
        Проверка, что созданный пользователь изначально не является суперпользователем и не входит в staff.
        """
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.is_staff)

    def test_user_is_superuser_view_promotes_user(self):
        """
        Проверка, что вызов представления user_is_superuser поднимает флаги is_superuser и is_staff,
        и возвращает корректный шаблон и статус.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('users_app:user_is_superuser'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users_app/my_account.html')

        self.user.refresh_from_db()
        self.assertTrue(self.user.is_superuser, "Пользователь не стал суперпользователем")
        self.assertTrue(self.user.is_staff, "Пользователь не получил статус staff")
