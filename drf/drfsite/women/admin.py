from django.contrib import admin
from .models import *

# Register your models here.


class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'time_updated', 'is_published', 'cat')
    list_editable = ('is_published', )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Women, WomenAdmin)
admin.site.register(Category, CategoryAdmin)
