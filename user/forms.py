from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class CustomAuthenticationForm(forms.Form):
    username_or_email = forms.CharField(
        max_length=254,
        widget=forms.TextInput(attrs={'placeholder': 'Имя пользователя или Email'})
    )
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def clean(self):
        username_or_email = self.cleaned_data.get('username_or_email')
        password = self.cleaned_data.get('password')

        if username_or_email and password:
            user = authenticate(username=username_or_email, password=password)
            if user is None:
                raise forms.ValidationError("Неверные данные. Проверьте имя пользователя/почту и пароль.")
            self.cleaned_data['user'] = user
        return self.cleaned_data

    def get_user(self):
        return self.cleaned_data.get('user')


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Обязательное поле.')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
