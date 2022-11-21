from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
from .models import Design, Category


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput, validators=[RegexValidator(r'[a-zA-Z\-]',
                                                                                                 'доступны'
                                                                                                 ' только латинские'
                                                                                                 ' символы')],
                               required=True)

    full_name = forms.CharField(label='ФИО', widget=forms.TextInput,
                                validators=[RegexValidator(r'[а-яА-ЯёЁ\-\s]',
                                                           'В ФИО доступна только кириллица, пробелы и дефис')],
                                required=True)

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput, required=True)
    email = forms.EmailField(label='Email', widget=forms.EmailInput, required=True,
                             validators=[EmailValidator('Email не верен')])
    checkbox = forms.CharField(label='Согласие на обработку персональных данных', widget=forms.CheckboxInput,
                               required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'full_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

    def clean_checkbox(self):
        cd = self.cleaned_data
        print(cd['checkbox'])
        # без использования False
        if not cd['checkbox']:
            raise forms.ValidationError('Подтвердите обработку персональных данных')
        return cd['checkbox']


class PostForm(forms.ModelForm):

    def clean_image(self):
        image = self.cleaned_data.get('image', False)
        if image:
            if image.size > 2 * 1024 * 1024:
                raise ValidationError("Вес картинки больше 2мб")
            return image
        else:
            raise ValidationError("Не возможно обработать картинку")

    class Meta:
        model = Design
        fields = ['name', 'info', 'image', 'category']


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name']

