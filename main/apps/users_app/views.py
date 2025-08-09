from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, EditUserForm
from .models import User
import uuid
import os


def login_telegram(request):
    if request.user.is_authenticated:
        return redirect('main_app:index')
    token = request.COOKIES.get('token')
    if token is None:
        token = str(uuid.uuid4())
    else:
        user = User.objects.filter(token=token).first()
        if user:
            login(request, user)
            response = redirect('main_app:index')
            response.delete_cookie('token')  # Удалить существующий куки
            return response
    context = {'TELEGRAM_BOT_NAME': os.getenv("TELEGRAM_BOT_NAME"), 'token': token}
    response = render(request, 'users_app/login.html', context)
    response.set_cookie('token', token, max_age=60 * 60 * 12)  # Ставим куки на 12 часов
    return response


def login_view(request):
    if request.user.is_authenticated:
        return redirect('main_app:index')
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = redirect('main_app:index')
            return response
        else:
            context = {'error': True}
            return render(request, 'users_app/login.html', context)
    else:
        return login_telegram(request)


def logout_view(request):
    logout(request)
    return render(request, 'main_app/index.html')


def register(request):
    '''Регистрирует нового пользователя.'''
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            login(request, new_user)
            return redirect('main_app:index')
        else:
            context = {'error': True, 'form': form}
            return render(request, 'users_app/register.html', context)
    else:
        form = RegisterForm()
    context = {'form': form}
    return render(request, 'users_app/register.html', context)


@login_required()
def edit_user(request):
    '''Личный кабинет.'''
    user = request.user
    if request.method != 'POST':
        form = EditUserForm(instance=user)
    else:
        form = EditUserForm(instance=user, data=request.POST)
        if form.is_valid():
            edit_user = form.save(commit=False)
            edit_user.save()
            return redirect('main_app:index')

    context = {'user': user,'form': form}
    return render(request, 'users_app/edit_user.html', context)


@login_required()
def my_account(request):
    '''Личный кабинет.'''
    return render(request, 'users_app/my_account.html')

@login_required()
def user_is_superuser(request):
    '''СТАТЬ СУПЕРПОЛЬЗОВАТЕЛЕМ.''' # ФУНКЦИЯ ДЛЯ УДОБСТВА ОЗНАКОМЛЕНИЯ С КОДОМ
    user = request.user
    user.is_superuser = True # стать СУПЕРПОЛЬЗОВАТЕЛЕМ
    user.is_staff = True  # получить доступ к АДМИНКЕ
    user.save()
    return render(request, 'users_app/my_account.html')