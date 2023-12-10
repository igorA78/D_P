import secrets
import string

from django.conf import settings
from django.contrib.auth.views import PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from users.forms import UserRegisterForm, UserProfileForm, CustomPasswordResetForm
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:confirm_email_start')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.auth_key = generate_new_key(8)
        user.save()
        send_mail(
            'Подтверждение регистрации',
            f'Вы зарегистрировались на сайте. Пройдите по ссылке, чтобы подтвердить регистрацию:\n'
            f'{get_current_site(self.request).domain}/users/confirm_email?key={user.auth_key}',
            settings.EMAIL_HOST_USER,
            [user.email]
        )
        return super().form_valid(form)


def confirm_email(request):
    url_key = request.GET.get('key')
    user = User.objects.filter(auth_key=url_key).first()
    if user:
        user.is_active = True
        user.save()
        return render(request, 'users/confirm_email_success.html')
    return render(request, 'users/confirm_email_error.html')


def confirm_email_start(request):
    return render(request, 'users/confirm_email.html')


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('catalog:index')

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_key(length=8):
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for i in range(length))


def password_reset(request):
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            user = User.objects.get(email=request.POST['email'])
            new_pass = generate_new_key()
            user.set_password(new_pass)
            user.save()
            send_mail(
                'Сброс пароля',
                f'Старый пароль сброшен. Для входа используйте новый пароль:\n'
                f'{new_pass}',
                settings.EMAIL_HOST_USER,
                [user.email]
            )
            return redirect('users:password_reset_done')
    else:
        form = CustomPasswordResetForm

    return render(request, 'users/password_reset.html', {'form': form})


def password_reset_done(request):
    return render(request, 'users/password_reset_done.html')

