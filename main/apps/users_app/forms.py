from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from phonenumber_field.formfields import PhoneNumberField

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username",)



class EditUserForm(forms.ModelForm):
    number = PhoneNumberField(region="RU")
    class Meta:
        model = User
        fields = ("username", "phone_number", "email",)
        labels = {'phone_number':'номер телефона'}
        widgets = {'phone_number':forms.TextInput(attrs={'cols': 60,
                                                         'rows': 1,
                                                         'placeholder':'+7 999 1234567',})}




