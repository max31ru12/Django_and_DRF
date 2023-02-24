from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField
from .models import *


# Прописываю класс формы, тесно свзяанной с моделью
class AddPostForm(forms.ModelForm):
    # Тут мы прописываем конструктор класса
    def __init__(self, *args, **kwargs):
        # Здесь мы вызываем конструктор родительского класса с помощью метода super()
        super().__init__(*args, **kwargs)
        # После вызоыва конструктора базового класса открывается доступ к fields['cat'].empty_label
        self.fields['cat'].empty_label = "Категория не выбрана"

    class Meta:
        # Выбираем, с какой моделью будет связана форма
        model = Women
        # Показывать все поля, кроме тех, что заполняются автоматически
        # # Рекомендуется явно указывать поля, поэтому запись будет другая
        # fields = '__all__'
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']
        # Далее можем определить стили для полей с помощью словаря widjets
        widjets = {'title': forms.TextInput(attrs={'class': 'form-input'}),
                   'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
                   }

    # Создаю валидатор, который должен начинаться с clean_ + то поле, для которого делаем валидацию
    def clean_title(self):
        # Получаем из словаря cleaned_data['title'] данные поля title
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')

        return title


class AddCategoryForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Categories
        fields = '__all__'


class RegisterUserForm(UserCreationForm):
    # переопределение полей, чтобы задать им виджеты
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))

    # Расширяем модель с помощь данного класса
    class Meta:
        # Определяем стандартную модель User
        model = User
        fields = ('username', 'password1', 'password2', 'email')
        # В Django виджеты для полей кроме username не работают, проэтому их нужно переопределять
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        }


# Наследуем от базового класса
class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Ваше имя', max_length=128)
    email = forms.EmailField(label='Ваш email')
    content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    # Это поле для стандартной капчи
    captcha = CaptchaField()

# # Класс формы
# # Это вариант с, по факту, дублированием кода, это не хорошо
#
# # Название класса придумываем сами, наследуется от базового класса
# class AddPostForm(forms.Form):
#     # Атрибуты - это поля, которые будут отображаться у нас в форме
#     # Мы собираемся делать форму, добавляющую статью в модель Women, поэтому поля должны повторять поля модели Wome
#     # за исключение time created и upadated, они добавляются автоматически
#     # widget=forms.TextInput(attrs={'class': 'form-input'} - этот атрибут добавит класс для нашего поля
#     title = forms.CharField(max_length=128, label='Заголовок',
#                             widget=forms.TextInput(attrs={'class': 'form-input'}))
#     # Атрибут label отвечает за имя поля формы на сайте
#     slug = forms.SlugField(max_length=255, label='URL')
#     content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Описание поста')
#     # Формирует чек-бокс о публикации,
#     # required=False (поле необязательное), по умолчанию True
#     # initial=True по умолчанию делает это поле отмеченным
#     is_published = forms.BooleanField(label='Публикация', required=False,
#                                       initial=True)
#     # Для выбора категории используется класс forms.ModelChoiseField
#     # Будет показывать выпадающий список, где мы будем выбирать соответствующие категории
#     # Список будет формировать на основе аргумента queryset, в который мы пихаем Categories.objects.all()
#     # empty_label отвечает за тот случай, когда ничего не выбрано
#     cat = forms.ModelChoiceField(queryset=Categories.objects.all(), label='Категория',
#                                  empty_label='Категория не выбрана')
#
#


