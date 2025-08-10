from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from phonenumber_field.formfields import PhoneNumberField

class RegisterForm(UserCreationForm):
    """
    Форма регистрации пользователя.
    """
    class Meta:
        model = User
        fields = ("username",)



class EditUserForm(forms.ModelForm):
    """
    Форма редактирования данных пользователя.
    """
    class Meta:
        model = User
        fields = ("username", "phone_number", "email",)
        widgets = {'phone_number':forms.TextInput(attrs={'cols': 13,
                                                         'rows': 1,
                                                         'placeholder':'+7 999 0000000',})}




