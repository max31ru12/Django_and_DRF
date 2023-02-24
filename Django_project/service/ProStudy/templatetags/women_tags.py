from django import template
from ProStudy.models import *

# Регистрация собсвенных тэгов
register = template.Library()


# Декоратор, который превращает функцию в тег (можно прописать атрибут name=)
# чтобы get_categories можно было вызывать в базовом шаблоне по другому имени
@register.simple_tag()
# функция для работы простого тега
def get_categories():
    # Возвращаем коллекцию QuerySet
    return Categories.objects.all()


@register.simple_tag()
def get_posts():
    return Women.objects.all()


# Включающий тег (можно сформировать список, а потом включать его куда надо)
@register.inclusion_tag('ProStudy/list_categories.html')
def show_categories():
    cats = Categories.objects.all()
    return {'cats': cats}

# Почему-то эта хрень работает только для base_page.html {% show_categories %}
# Можно написать туда {% show_categories %} и все появится
