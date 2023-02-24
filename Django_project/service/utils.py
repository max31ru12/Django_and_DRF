# Это файл с дополнительными вспомогательными классами
from ProStudy.models import *
from django.core.cache import cache

menu = [
        {'title': 'Главная', 'url_name': 'homepage'},
        {'title': 'Категории', 'url_name': 'categories'},
        {'title': 'Добавить кат', 'url_name': 'add_cat'},
        {'title': 'Добавить статью', 'url_name': 'add_post'},
        {'title': 'Обратная связь', 'url_name': 'contact'},
        ]


# Прописываю вспомогательный класс для views
class DataMixin:
    def get_user_context(self, **kwargs):
        # Формируем словарь из параметров, которые были переданы этой функции
        context = kwargs
        # Включаем кэширование для cats используя API низкого уровня
        cats = cache.get('cats')
        if not cats:
            cats = Categories.objects.all()
            cache.set('cats', cats, 60)

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop()

        context['menu'] = user_menu
        context['cats'] = cats
        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context

