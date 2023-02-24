from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *

# Register your models here.


# В админке отобразить все поля из БД (Надо зарегистрировать вместе с классом)
class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'photo', 'is_published', 'cat')
    # Поля, на которые можно кликнуть и перейти на соответствующую статью
    list_display_links = ('id', 'title')
    # По каким полям можно производить поиск
    search_fields = ('title', 'content')
    # Редактируемое поле из списка статей
    list_editable = ('is_published', )
    # Список поле, по которым можно фильтровать из админ панели (вручную указывать)
    list_filter = ('is_published', 'time_create', )
    prepopulated_fields = {'slug': ("title", )}




class CategoriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_description', 'slug')
    list_display_links = ('id', 'name',)
    search_fields = ('name',)
    # С помощью этого атрибута можем указать заполять автоматически поле, например, slug на основе поля name
    prepopulated_fields = {'slug': ("name",)}


# Регистрируем модель для админ панели
admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Women, WomenAdmin)
