from django.urls import path, include
from . import views

app_name = 'users_app'
urlpatterns = [
    path('login/', views.login_view, name='login'), # страница авторизации
    path('register/', views.register, name='register'), # страница регистрации
    path('logout', views.logout_view, name='logout'),   # выход пользователя
    path('my_account', views.my_account, name='my_account'),    # страница профиля
    path('edit_user/', views.edit_user, name='edit_user'),      # редактирование профиля
    path('user_is_superuser', views.user_is_superuser, name='user_is_superuser'),   # стать суперпользователем
]