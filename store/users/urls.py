from django.contrib.auth.decorators import login_required
from django.urls import path

from users.views import login, logout, UserProfileView, UserRegistrationView


app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('profile/<int:pk>/', login_required(UserProfileView.as_view()), name='profile'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
]
