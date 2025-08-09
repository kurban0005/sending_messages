from django.urls import path, include
from . import views

app_name = 'users_app'
urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('logout', views.logout_view, name='logout'),
    path('my_account', views.my_account, name='my_account'),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('my_account', views.my_account, name='my_account'),
    path('user_is_superuser', views.user_is_superuser, name='user_is_superuser'),
]