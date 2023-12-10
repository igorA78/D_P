from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm, PasswordResetForm

from catalog.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', )


class UserLoginForm(StyleFormMixin, AuthenticationForm):

    class Meta:
        model = User


class UserProfileForm(StyleFormMixin, UserChangeForm):

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'avatar', 'phone', 'country')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class CustomPasswordResetForm(StyleFormMixin, forms.Form):
    email = forms.EmailField()

    def clean(self):
        cleaned_data = super().clean()
        user_email = cleaned_data.get('email')

        if not User.objects.filter(email=user_email).first():
            raise forms.ValidationError('Нет пользователя с такой почтой')

        return cleaned_data


