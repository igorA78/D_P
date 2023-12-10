from django import forms

from catalog.models import Product, UserQuestion, Harvest



class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            if isinstance(field.widget, forms.widgets.Textarea):
                field.widget.attrs['rows'] = 3
            if isinstance(field.widget, forms.widgets.CheckboxInput):
                field.widget.attrs['class'] = 'form-check-input m-2'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('created_at', 'changed_at', 'owner', )
        labels = {
            'name': 'Наименование',
            'description': 'Описание',
            'image': 'Изображение',
            'category': 'Категория',
            'price': 'Цена (Руб.)',
        }


class UserQuestionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = UserQuestion
        exclude = ('created_at',)
        labels = {
            'user_name': 'Ваше имя',
            'phone': 'Телефон для связи',
            'email': 'Почта для связи',
            'question': 'Ваш вопрос',
        }

class HarvestForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Harvest
        fields = '__all__'

    def clean_is_current(self):
        cleaned_data = self.cleaned_data['is_current']

        print(len(self.cleaned_data['product'].harvest_set.filter(is_current=True)))
        if (cleaned_data):
            if len(self.cleaned_data['product'].harvest_set.filter(is_current=True)) > 0:
                raise forms.ValidationError('Может быть только одно текущее обращение!')

        return cleaned_data
