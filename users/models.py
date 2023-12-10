from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'null': 'True', 'blank': 'True'}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')

    avatar = models.ImageField(upload_to='users/', **NULLABLE, verbose_name='аватар')
    phone = models.CharField(max_length=35, **NULLABLE, verbose_name='телефон')
    country = models.CharField(max_length=50, **NULLABLE, verbose_name='страна')
    auth_key = models.CharField(max_length=150, verbose_name='ключ верификации почты', default='qwerty')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

