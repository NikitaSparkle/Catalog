from django import forms

from .models import *


class SingUpForm(forms.Form):
    email = forms.EmailField(label="Электронная почта", required=True)
    phone = forms.CharField(label="Номер телефона", required=True, max_length=32)
    country = forms.ModelChoiceField(label="Страна", queryset=Country.objects.filter(), required=True)
    password = forms.CharField(label="Пароль", max_length=16, required=True)
    password1 = forms.CharField(label="Повторите пароль", max_length=16, required=True)


class LoginForm(forms.Form):
    username = forms.CharField(label="Email", required=True)
    password = forms.CharField(label="Пароль", max_length=16, required=True)
    next = forms.CharField(widget=forms.HiddenInput(), required=False)


class ConfirmForm(forms.Form):
    code = forms.CharField(label="Код")
