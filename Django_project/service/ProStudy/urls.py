from django.urls import path, re_path, include
from .views import *
from django.views.decorators.cache import cache_page

# Пишем декоратор cache_page, в скобочках пишем время кэширования (сколько будет храниться кэш)
# а дальше в других скобочках пишем декорируемый класс или функцию
# cache_page(60)(WomenHome.as_view())

urlpatterns = [
    # Записываю класс WomenHome вместо функции представления, затем у класса вызываю функицю as_view
    # Когда функция без скобок - это функция на ссылку, когда со скобками - это вызов функции
    path('', cache_page(60)(WomenHome.as_view()), name='homepage'),
    path('add_post/', AddPost.as_view(), name='add_post'),
    path('categories/', WomenCategories.as_view(), name='categories'),
    path('add_cat/', AddCategory.as_view(), name='add_cat'),
    path('contact/', ContactFormView.as_view(), name='contact'),
    # Меняет вместо отобрадение идентификатора на отобрадение по slug
    # path('post/<int:post_id>/', show_post, name='post'),
    # Тогда во вьюшках переменная будет не post_id, а post_slug
    path('category/<slug:cat_slug>/', WomenPost.as_view(), name='post'),
    path('<slug:post_slug>/', ShowPost.as_view(), name='show_post'),
    path('/register', RegisterUser.as_view(), name='register'),
    path('/login', LoginUser.as_view(), name='login'),
    path('/logout', logout_user, name='logout'),

]
