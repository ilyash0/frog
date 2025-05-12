from django import forms
from .models import User, Frog


class GiftFrogForm(forms.Form):
    recipient_username = forms.CharField(
        max_length=150,
        label='Имя получателя',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите имя пользователя получателя',
        })
    )

    frog = forms.ModelChoiceField(
        queryset=Frog.objects.none(),
        label='Лягушка',
        empty_label='Выберите вашу лягушку',
        widget=forms.Select()
    )

    message = forms.CharField(
        label='Сообщение к подарку',
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Введите ваше сообщение (необязательно)',
            'rows': 3,
        })
    )
    confirm = forms.BooleanField(
        label='Я понимаю, что я больше не увижу эту лягушку',
        widget=forms.CheckboxInput()
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields['frog'].queryset = user.frog_set
        else:
            self.fields['frog'].queryset = Frog.objects.none()

    def clean_recipient_username(self):
        username = self.cleaned_data['recipient_username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError(f"Пользователь «{username}» не найден.")
        return username

    def get_recipient(self):
        return User.objects.get(username=self.cleaned_data['recipient_username'])