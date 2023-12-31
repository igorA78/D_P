# Generated by Django 4.2.7 on 2023-12-10 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_alter_harvest_options_harvest_harvest_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='harvest',
            name='harvest_date',
            field=models.DateField(verbose_name='Дата регистрации обращения'),
        ),
        migrations.AlterField(
            model_name='harvest',
            name='is_current',
            field=models.BooleanField(default=False, verbose_name='Активное обращение (да/нет)'),
        ),
    ]
