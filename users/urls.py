from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from users.apps import UsersConfig
from users.forms import UserLoginForm
from users.views import RegisterView, ProfileView, password_reset, password_reset_done, confirm_email, confirm_email_start

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(template_name='users/login.html', authentication_form=UserLoginForm), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password_reset/', password_reset, name='password_reset'),
    path('password_reset_done/', password_reset_done, name='password_reset_done'),
    path('confirm_email/', confirm_email, name='confirm_email'),
    path('confirm_email_start/', confirm_email_start, name='confirm_email_start'),
]
