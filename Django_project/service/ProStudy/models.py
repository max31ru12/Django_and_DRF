from django.db import models
from django.urls import reverse
# from django.utils import timezone

# Консольные команды для записи данных в БД
# python .\manage.py shell
# from ProStudy.models import Mailing
# Mailing(text = 'Первый текст')
# w1 = _ сохраняет последние изменения
# w1.save()
#
# Create your models here.

# Посмотреть SQL-запрос для создание такой таблицы
# from django.db import connection
# connection.queries
# # q4 = Mailing.objects.create(text = 'fourth text') - сразу добавляет данные в БД
#
# class Women(models.Model):
#     title = models.CharField(max_length=128) # max_length - обязательный аргумент
#     content = models.TextField(blank=True) # blank = True - поле может быть пустым (по умолчанию - False)
#     photo = models.ImageField(upload_to="photos/%Y/%m/%d")
#     time_create = models.DateTimeField(auto_now_add=True)
#     time_update = models.DateTimeField(auto_now=True)
#     is_published = models.BooleanField(default=False)


# В БД автоматически добавляется _id, то есть получится category_id
# 'Categories' в кавычках, потому что класс Categories определен после всех моделей
# Категории курсов
# verbose_name - имя столбца таблицы в админ-панели
class Women(models.Model):
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    # На данном этапе добавляется slug с помощью SlugField
    # db_index=True - индексируемое поле, поиск по слагу будет происходить быстрее
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = models.TextField(blank=True, verbose_name='Текст статьи')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d", verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=False, verbose_name='Публикация')
    # null = Nrue - можно заполнять нулями
    cat = models.ForeignKey('Categories', on_delete=models.CASCADE, null=True, verbose_name='Категория')

    def __str__(self):
        return self.title

    # Функция возвращает абсолютный адрес для записи в таблице Women
    # Класс представления для форм, унаследованный от CreateView, ватоматически
    # берет post_slug из параметра kwargs
    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    # Специальный класс, который используется админ-панелью, для настройки (отображения) данной модели
    class Meta:
        # Для едиственного числа
        verbose_name = 'Известные женщины'
        # Для множественного числа
        verbose_name_plural = 'Известные женщины'
        # Сортировка по полю title (-title - Обратный порядок)
        ordering = ['id']


class Categories(models.Model):
    # db_index - поле будет индексировано, поиск по нему будет происходить быстрее
    name = models.CharField(max_length=128, db_index=True, verbose_name='Категория')
    short_description = models.TextField(max_length=256, blank=True, verbose_name='Короткое описание')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.name

    # Функция необходима для просмотра на сайте моделей в панели админа
    def get_absolute_url(self):
        return reverse('category', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'
        ordering = ['id']
# в 'Categories' нет никаких записей, значить надо прописать в ForeignKey null=True (временно)

# Добавить Категории

# python manage.py shell
# from ProStudy.models import *
# Categories.objects.create(name = 'Программирование') - создаем новую запись
# w_list = git.objects.all() - переменная w_list будет ссылаться список всех записей
# w_list.update(category_id = 1) - изменим значение поля category на значение = 1

# Связи

# ForeignKey - для связей Many to one (поля отношений)
# ManyToManyField - для связей Many to Many (многие ко многим)
# OneToOneField - для всязей One to One (один к одному)

# ForeignKey обязательные аргументы:
# ForeignKey(<ссылка на первичную модель>, on_delete = <ограничения при удалении>)

# <ограничения при удалении:

# models.CASCADE - удаление всех записей из вторичной модели
# models.PROTECT - запрещает удаление первичной модели, если она используется во вторичной
# models.SET_NULL - при удалении записи первичной модели устанавливает значение foreign key В Null
# models.у соответствующих значений вторичной модели
# models.SET_DEFAULT - то же самое, что и SET_NULL, то ставит дефолтное значение
# models.SET() - то же самое, только устанавливает пользовательское значение
# models.DO_NOTHING - удаление записи в первичной модели не вызывает никаких действий у вторичных моделей




# Django ORM

# Women.objects.all()[3:8] - берет 5 записей с 3 по 8
# Women.objects.order_by('pk') - вывести все значения, отсортированные по 'pk' то есть по id
# Women.objects.order_by('-pk') - противоположный порядок
# Women.objects.all().reverse() - выбрать все записи в обратном порядке
# Women.objects.filter(pl__lte=2) - выбрать все записи, где pk <= 2
# Women.objects.get(pk=2) - возвращается не QuerySet, а экземпляр модели Women
#
# w = Women.objects.all(): 1) Доступны все поля от title до is_published
#                          2) Идентификатор записи (первичный ключ) w.pk или w.id
#                          3) w.cat_id - идентификатор рубрики (внешний ключ)
#                          4) w.cat - объект класса Categories, хранящий данные записи с id = cat_id
#
# с = Categories.objects.get(pk=1) - получаю категорию актрисы
# c.women_set.all() - получаю все экземпляры модели women, связанные с актрисами
#
# <вторичная модель>_set
# <имя_атрибута>__gte - больше или равно (>=)
# <имя атрибута>__lte - меньше или равно (<=) tt - меньше (<)
#
# Women.objects.filter(title__contains='ли') - выбрать все записи, где в поле title встречается 'ли'
# Women.objects.filter(title__contains='ли') - то же самое, только без учета регистра (но с sqlite не работает)
# Women.objects.filter(pk__in=[2,5,11,12]) - выбрать где pk в этих значениях
# Women.objects.filter(pk__in=[2,5,11,12], is_published=True) - истинно и это и это условие (AND)
#
# Класс Q, его надо импортировать
# from django.db.models import Q
# Women.objects.filter(Q(pk__lt=5) | Q(cat_id=2)) - так прописывается шаблон ИЛИ
# Women.objects.filter(Q(pk__lt=5) & Q(cat_id=2)) - так прописывается шаблон И
# Women.objects.filter(Q(pk__lt=5) | Q(cat_id=2)) - так прописывается шаблон ИЛИ
# Women.objects.filter(~Q(pk__lt=5) | Q(cat_id=2)) - так прописывается ~Q(pk__lt=5) НЕ (Q(УСЛОВИЕ))
# Women.objects.order_by('pk').first() - выберет первую запись
# Women.objects.order_by('pk').last() - выберет последнюю запись
# Women.objects.latest('time_update') - выбрать запись с самой поздней датой
# Women.objects.earliest('time_update') - выбрать запись с ранней датой
# w = Women.objects.get(pk=7)
# w.get_previous_by_time_update() - искать предыдущую запись по полю time_update
# w.get_next_by_time_update() - искать следующую запись по полю time_update
# w.get_next_by_time_update(pk__gt=10) - искать следующую запись по полю time_update с pk > 10
#
# c2 = Categories.objects.get(pk=2)
# c2.women_set.exists() -> False или True (Пустая или не пустая рубрика)
# c2.women_set.count() -> Сколько женщин есть в категории с pk = 2
# Women.objects.filter(pk__gt).count() - сколько женщин с id > 4
# Women.objects.filter(cat__slug='aktrisy') - выбрать женщин, у которых слаг категории - это актрисы
# Women.objects.filter(cat__in=[1]) - берем категорию 1
# Women.objects.filter(cat_name__contains('ы')) - имя категории содержит 'ы'
# Category.objects.filter(women__title__contains('ли')) - выбрать категорию, где есть певицы с 'ли' в имени
#
#
# Команды агрегации
# Women.objects.count() - Считает все записи
# Women.objects.aggregate(Min('cat_id')) - Чему равно мин. значение поля cat_id
# Women.objects.aggregate(Min('cat_id'), Max(cat__id))
# Women.objects.aggregate(res=Sum('cat_id') - Count('cat_id'))
# Women.objects.aggregate(Avg('cat_id'))
#
# Women.objects.filter(pk__gt=4).aggregate(Avg('cat_id')) - берем сначала фильтр, затем агрегацию
#
# Women.objects.values('cat_id').annotate(Count('id'))
# .values('cat_id') == GROUP BY cat_id
# .annotate(Count('id)) == SELECT COUNT(id)
# SELECT count(id) FROM women GROUP BY cat_id
# В итоге эта хрень даст какую-то дичь, потому что в модели прописано ordering
#
# Category.objects.annotate(total=Count('women')).filter(total__gt=0) - Выбрать те категории, где есть больше 0 женщин
# то есть по сути через .annotate() создаем total = Count('women'), считаем всех женщин, относящихся к категории
# затем фильтруем уже по total
#
#
# Класс F
# from django.db.models import F
# Можем прописывать нужные нам поля, то есть
# Women.objects.filter(pk__gt=F('cat')) - выбрать значения, где id больше чем id категории
#
# raw SQL queries
# Women.objects.raw(SELECT * FROM women_women)
#
#
#
#
#
#
#
#
#
#
#
#
#
