from datetime import date

from django.db import models

from users.models import User

NULLABLE = {'null': 'True', 'blank': 'True'}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']


class Product(models.Model):
   # user_admin = User.objects.filter(is_superuser=True).first().pk

    name = models.CharField(max_length=100, verbose_name='Наименование')
    description = models.TextField(verbose_name='Описание', **NULLABLE)
    image = models.ImageField(upload_to='products/', verbose_name='Изображение', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='id категории')
    price = models.IntegerField(verbose_name='Цена', **NULLABLE)
    created_at = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    changed_at = models.DateField(verbose_name='Дата изменения', auto_now=True)
      #  owner = models.ForeignKey(User, on_delete=models.SET_DEFAULT, default=user_admin, verbose_name='Автор')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    is_published = models.BooleanField(verbose_name='Опубликовано (да/нет)', default=False)

    def __str__(self):
        return f'{self.name}'

    @property
    def current_harvest(self):
        return self.harvest_set.filter(is_current=True).last()

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        ordering = ['category', 'name']
        permissions = [
            (
                'moderator',
                'can change is_published, description, category'
            )
        ]


class CompanyContact(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    icon_bootstrap = models.CharField(max_length=100, verbose_name='Иконка Bootstrap')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'


class UserQuestion(models.Model):
    user_name = models.CharField(max_length=150, verbose_name='Имя')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Почта')
    question = models.TextField(verbose_name='Вопрос')
    created_at = models.DateField(verbose_name='Дата', auto_now_add=True)

    def __str__(self):
        return f'{self.user_name}: {self.question[:20]}'

    class Meta:
        verbose_name = 'Вопрос пользователя'
        verbose_name_plural = 'Вопросы пользователей'


class Harvest(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Услуга')
    harvest_description = models.TextField(verbose_name='Описание', **NULLABLE)
    harvest_number = models.IntegerField(verbose_name='Номер')
    harvest_date = models.DateField(verbose_name='Дата регистрации обращения')
    is_current = models.BooleanField(default=False, verbose_name='Активное обращение (да/нет)')

    def __str__(self):
        return f'({self.harvest_number}) {self.harvest_date} - {self.product}'

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'
