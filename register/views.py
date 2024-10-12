from django.shortcuts import render, redirect

from payapp.models import Account
from .forms import RegisterForm
from django.contrib.auth import login

from payapp.models import get_account_default

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'register/register.html', { 'form': form})   
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            Account.objects.create(user=user, currency=form.cleaned_data['currency'], amount=get_account_default(form.cleaned_data['currency']))
            login(request, user)
            return redirect('homepage')
        else:
            return render(request, 'register/register.html', {'form': form})



