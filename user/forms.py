from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

        labels = {
            'username': 'Имя пользователя',
            'email': 'Почта',
            'password1': 'Пароль',
            'password2': 'Подтверждение пароля',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['username', 'email', 'password1', 'password2']:
            self.fields[field_name].help_text = ''


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email')

        labels = {
            'username': 'Имя пользователя',
            'email': 'Электронная почта',
        }
