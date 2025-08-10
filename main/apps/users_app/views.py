from typing import Optional
from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from .forms import RegisterForm, EditUserForm
from .models import User
import uuid
import os


def login_telegram(request: HttpRequest) -> HttpResponse:
    """
    Обрабатывает вход пользователя через Telegram.

    Если пользователь уже аутентифицирован, перенаправляет на главную страницу.
    Иначе пытается получить токен из cookie, создать нового или авторизовать пользователя по токену.
    Устанавливает cookie с токеном на 12 часов.

    :param request: Объект HTTP-запроса.
    :return: HTTP-ответ с рендерингом страницы входа или редиректом.
    """
    if request.user.is_authenticated:
        return redirect('main_app:index')

    token: Optional[str] = request.COOKIES.get('token')
    if token is None:
        token = str(uuid.uuid4())
    else:
        user = User.objects.filter(token=token).first()
        if user:
            login(request, user)
            response = redirect('main_app:index')
            response.delete_cookie('token')  # Удалить существующий cookie
            return response

    context = {'TELEGRAM_BOT_NAME': os.getenv("TELEGRAM_BOT_NAME"), 'token': token}
    response = render(request, 'users_app/login.html', context)
    response.set_cookie('token', token, max_age=60 * 60 * 12)  # Устанавливаем cookie на 12 часов
    return response


def login_view(request: HttpRequest) -> HttpResponse:
    """
    Обрабатывает стандартный вход пользователя по логину и паролю.

    При успешной аутентификации перенаправляет на главную страницу.
    При неудаче отображает страницу входа с ошибкой.
    Если метод запроса не POST, делегирует обработку в login_telegram.

    :param request: Объект HTTP-запроса.
    :return: HTTP-ответ с рендерингом страницы входа или редиректом.
    """
    if request.user.is_authenticated:
        return redirect('main_app:index')

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('main_app:index')
        else:
            context = {'error': True}
            return render(request, 'users_app/login.html', context)

    return login_telegram(request)


def logout_view(request: HttpRequest) -> HttpResponse:
    """
    Выполняет выход пользователя из системы и отображает главную страницу.

    :param request: Объект HTTP-запроса.
    :return: HTTP-ответ с рендерингом главной страницы.
    """
    logout(request)
    return render(request, 'main_app/index.html')


def register(request: HttpRequest) -> HttpResponse:
    """
    Регистрирует нового пользователя.

    Обрабатывает POST-запрос с данными формы регистрации.
    При успешной регистрации выполняет вход и перенаправляет на главную страницу.
    При ошибках отображает форму с ошибками.

    :param request: Объект HTTP-запроса.
    :return: HTTP-ответ с рендерингом страницы регистрации или редиректом.
    """
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('main_app:index')
        else:
            context = {'error': True, 'form': form}
            return render(request, 'users_app/register.html', context)

    form = RegisterForm()
    context = {'form': form}
    return render(request, 'users_app/register.html', context)


@login_required()
def edit_user(request):
    """
    Отображает и обрабатывает форму редактирования профиля пользователя.

    При GET-запросе отображает форму с текущими данными пользователя.
    При POST-запросе валидирует и сохраняет изменения, затем перенаправляет на главную страницу.
    :param request: Объект HTTP-запроса.
        :return: HTTP-ответ с рендерингом страницы редактирования профиля или редиректом.
        """
    user = request.user
    if request.method != 'POST':
        form = EditUserForm(instance=user)
    else:
        form = EditUserForm(instance=user, data=request.POST)
        if form.is_valid():
            edit_user = form.save(commit=False)
            edit_user.save()
            return redirect('main_app:index')
        else:
            error = 'is_not_valid'
            context = {'user': user, 'form': form, 'error': error, }
            return render(request, 'users_app/edit_user.html', context)

    context = {'user': user, 'form': form}
    return render(request, 'users_app/edit_user.html', context)


@login_required()
def my_account(request: HttpRequest) -> HttpResponse:
    """
    Отображает страницу личного кабинета пользователя.

    :param request: Объект HTTP-запроса.
    :return: HTTP-ответ с рендерингом страницы личного кабинета.
    """
    return render(request, 'users_app/my_account.html')


@login_required()
def user_is_superuser(request: HttpRequest) -> HttpResponse:
    """
    Делает текущего пользователя суперпользователем и сотрудником (staff).

    Используется для удобства ознакомления с кодом.
    После изменения прав пользователя отображает страницу личного кабинета.

    :param request: Объект HTTP-запроса.
    :return: HTTP-ответ с рендерингом страницы личного кабинета.
    """
    user = request.user
    user.is_superuser = True  # Сделать суперпользователем
    user.is_staff = True  # Дать доступ к админке
    user.save()
    return render(request, 'users_app/my_account.html')
