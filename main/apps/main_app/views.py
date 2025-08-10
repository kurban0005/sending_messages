from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponse
from .notifications import send_all_notification, send_telegram_notification, send_email_notification, send_sms_notification


@login_required()
def index(request: HttpRequest) -> HttpResponse:
    """
    Отображает домашнюю страницу.

    :param request: Объект запроса.
    :return: Рендеринг страницы 'main_app/index.html'.
    """
    return render(request, 'main_app/index.html')


@login_required
def notify_user(request: HttpRequest) -> HttpResponse:
    """
    Отправляет все уведомления пользователю.

    :param request: Объект запроса.
    :return: Рендеринг страницы 'main_app/index.html'.
    """
    message = "This is a test notification!"
    send_all_notification(request.user, message)
    return render(request, 'main_app/index.html')


@login_required()
def sms_notification(request: HttpRequest) -> HttpResponse:
    """
    Отправляет SMS-уведомление пользователю.

    :param request: Объект запроса.
    :return: Рендеринг страницы 'main_app/index.html'.
    """
    message = "Это тестовое сообщение написано специально для вас!"
    send_sms_notification(request.user, message)
    return render(request, 'main_app/index.html')


@login_required()
def email_notification(request: HttpRequest) -> HttpResponse:
    """
    Отправляет email-уведомление пользователю.

    :param request: Объект запроса.
    :return: Рендеринг страницы 'main_app/index.html'.
    """
    message = "Это тестовое сообщение написано специально для вас!"
    send_email_notification(request.user, message)
    return render(request, 'main_app/index.html')


@login_required()
def telegram_notification(request: HttpRequest) -> HttpResponse:
    """
    Отправляет Telegram-уведомление пользователю.

    :param request: Объект запроса.
    :return: Рендеринг страницы 'main_app/index.html'.
    """
    message = "Это тестовое сообщение написано специально для вас!"
    send_telegram_notification(request.user, message)
    return render(request, 'main_app/index.html')