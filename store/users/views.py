from django.shortcuts import render

from users.forms import UserLoginForm
from users.models import User


def login(request):
    context = {
        'form': UserLoginForm(),
    }
    return render(request, 'users/login.html', context)


def registration(request):
    return render(request, 'users/registration.html')
