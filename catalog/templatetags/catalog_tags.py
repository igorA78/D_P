from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def bg_light_color(i=1):
    if i % 2 == 1:
        return 'bg-light-orange'
    else:
        return 'bg-light-green'


@register.simple_tag
def bg_dark_color(i=1):
    if i % 2 == 1:
        return 'bg-orange'
    else:
        return 'bg-dark-green'


@register.simple_tag
def text_color(i=1):
    if i % 2 == 1:
        return 'text-color-orange'
    else:
        return 'text-color-green'


@register.simple_tag
def mediapath(file_path):
    return f'{settings.MEDIA_URL}{file_path}'
