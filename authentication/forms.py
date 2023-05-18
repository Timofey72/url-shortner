from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if username:
            qs = User.objects.filter(username=username)
            if qs.exists():
                raise forms.ValidationError('Пользователь с таким именем уже существует!')

        if email:
            qs = User.objects.filter(email=email)
            if qs.exists():
                raise forms.ValidationError('Пользователь с таким email уже существует!')

        if password:
            if len(password) < 8:
                raise forms.ValidationError('Пароль должен содержать не меньше 8 символов!')

        return self.cleaned_data


class UserLoginForm(forms.Form):
    """Форма входа для пользователей"""
    username = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}), label='Имя пользователя')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='Пароль')

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username:
            user = User.objects.filter(username=username)
            if not user.exists():
                raise forms.ValidationError('Такого пользователя нет!')
            if not check_password(password, user.first().password):
                raise forms.ValidationError('Пароль не верный!')

        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )

        return self.cleaned_data

    def get_user(self):
        return self.user_cache
