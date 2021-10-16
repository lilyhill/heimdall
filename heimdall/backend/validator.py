from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import MyUser


class UserForm(forms.ModelForm):

    class Meta:
        model = MyUser
        fields = ['username', 'email', 'password']


class LoginForm(forms.Form):

    username = forms.CharField(max_length=100, required=True)
    password = forms.CharField(max_length=100, required=True)