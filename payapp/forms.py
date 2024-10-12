from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms

from .models import Account


class SendMoneyForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    amount = forms.DecimalField(max_digits=10, decimal_places=2)


class RequestMoneyForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    amount = forms.DecimalField(max_digits=10, decimal_places=2) 
