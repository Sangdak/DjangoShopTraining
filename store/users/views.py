from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import CommonTitleMixin
from products.models import Basket
from users.models import EmailVerification, User
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm


class UserRegistrationView(CommonTitleMixin, SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    model = User
    success_message = 'Вы успешно зарегистрированы!'
    success_url = reverse_lazy('users:login')
    template_name = 'users/registration.html'
    title = 'Store - Регистрация'


class UserProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    model = get_user_model()
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    extra_context = {'title': 'Store - Личный Кабинет'}

    def get_object(self, queryset=None):
        return self.request.user


class EmailVerificationView(CommonTitleMixin, TemplateView):
    title = 'Store - Подтвердение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs.get('code')
        user = User.objects.get(email=kwargs.get('email'))
        email_verifications = EmailVerification.objects.filter(code=code, user=user)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))
