"""drfsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from women.views import *
from rest_framework import routers

# # Создаем стандартный роутер
# # Есть два класса SimpleRouter и DefaultRouter, отличаются тем, что у DefaultFouter
# # есть маршрут ttp://127.0.0.1:8000/api/v1, а у SimpleRouter - нет
# router = routers.SimpleRouter()
# # Регистрируем наш ViewSet
# router.register(r'women', WomenViewSet)
# # router.register(r'women', WomenViewSet, basename='man')
# # basename - это префикс для формирования имени маршрута, по дефолту это дается имя модели

urlpatterns = [
    path('admin/', admin.site.urls),
    # Подключаем авторизацию на основе сессии, появляются маршруты
    # api/v1/drf-auth/login and api/v1/drf-auth/logout
    path('api/v1/drf-auth/', include('rest_framework.urls')),
    # Вручную прописываю маршруты
    path('api/v1/women/', WomenAPIList.as_view()),
    path('api/v1/women/<int:pk>/', WomenAPIUpdate.as_view()),
    path('api/v1/womendelete/<int:pk>/', WomenAPIDestroy.as_view()),
    # Подключаем djoser к проекту
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),


    # path('api/v1/', include(router.urls)) # http://127.0.0.1:8000/api/v1/women/
    # # Обрабатываем get-запрос с помощью метода list из документации
    # Два маршрута ниже можно переделать с помощью роутеров
    # path('api/v1/womenlist/', WomenViewSet.as_view({'get': 'list'})),
    # path('api/v1/womenlist/<int:pk>/', WomenViewSet.as_view({'put': 'update'})),

]
