from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import logout, UserLoginView, UserProfileView, UserRegistrationView


app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
]
