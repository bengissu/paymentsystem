# from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms

from payapp.models import Account

class RegisterForm(UserCreationForm):
    currency = forms.ChoiceField(choices=Account.CURRENCY_TYPES)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2', 'currency']

