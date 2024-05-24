from django.contrib import auth, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from common.views import CommonTitleMixin
from products.models import Basket
from users.models import User
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm


# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('index'))
#     else:
#         form = UserLoginForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'users/login.html', context)


class UserRegistrationView(CommonTitleMixin, SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    model = User
    success_message = 'Вы успешно зарегистрированы!'
    success_url = reverse_lazy('users:login')
    template_name = 'users/registration.html'
    title = 'Store - Регистрация'


# def registration(request):
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно зарегистрировались на сайте!')
#             return HttpResponseRedirect(reverse('users:login'))
#     else:
#         form = UserRegistrationForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'users/registration.html', context)
#


class UserProfileView(LoginRequiredMixin, UpdateView):
    form_class = UserProfileForm
    model = get_user_model()
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    extra_context = {'title': 'Store - Личный Кабинет'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['baskets'] = Basket.objects.filter(user=self.object)
        return context

    def get_object(self, queryset=None):
        return self.request.user


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(instance=request.user, data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('users:profile'))
#         else:
#             print(form.errors)
#     else:
#         form = UserProfileForm(instance=request.user)
#
#     baskets = Basket.objects.filter(user=request.user)
#
#     context = {
#         'title': 'Store - Профиль',
#         'form': form,
#         'baskets': baskets,
#     }
#     return render(request, 'users/profile.html', context)
#

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))
