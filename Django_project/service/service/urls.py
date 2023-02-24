"""service URL Configuration

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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from ProStudy.views import *
from service import settings
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    # URL для капчи
    path('captcha/', include('captcha.urls')),
    path('', include('ProStudy.urls')), # http://127.0.0.1:8000/ отсчитываются от доменного имени
]

# Если в файле settings переменная DEBUG == True, то
if settings.DEBUG:
    # Эту штуку мы делаем, чтобы закрепить debug_toolbar справа на странице
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls))
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
# handler404 = pageNotFound # Обработчику джанго указываем ипользовать функцию при ошибке 404
