from django import forms

from blog.models import Blog
from catalog.forms import StyleFormMixin


class BlogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Blog
        exclude = ('slug', 'created_at', 'views_count', 'owner',)
        labels = {
            'title': 'Заголовок статьи',
            'message': 'Текст статьи',
            'preview': 'Превью для статьи',
            'is_published': 'Опубликовано',
        }
