from django.contrib.auth import logout, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.views import LoginView
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404  # render - это встроенный шаблонизатор
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, FormView
# Это миксин для ограничения доступа неавторизованным пользователям
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from utils import *
from .forms import *
# Вспомогательные классы прописываются в ProStudy/utils.py
# Create your views here.


class WomenHome(DataMixin, ListView):
    # В ListView уже встроена пагинация (затем надо прописать в шаблоне что-то)
    # По сути paginate_by добавляет в context поле page_obj, которое берет какое-то кол-во записей из Women
    # Как я понял, надо работать с эьтой хуйней как с контекстом
    paginate_by = 20 # Эту строчку можно добавить в DataMixin
    model = Women
    # Указываю шаблон
    template_name = 'ProStudy/index.html'
    # Я передал в base_page ТЭГ {% get_posts as posts %}, но вместо этого и отсального я передал
    # коллекцию model = Women, поэтому нужно явно указать, что еще передаю templatetag posts
    context_object_name = 'posts'
    # Это я записываю поле context (можно передавать только статические данные)
    # extra_context = {'title': 'Онлайн-школа ProStudy'} перенес в метод get_context_data

    # Для передачи и статических, и динамических данных контекста используется такая функция
    def get_context_data(self, *, object_list=None, **kwargs):
        # Получаем уже существующие данные, то есть пишет эту штуку для того, чтобы не потерять
        # context_object_name = 'posts', то есть оставляет тот контекст, который уже есть
        context = super().get_context_data(**kwargs)
        # Здесь вызываем метод из DataMixin, и присваиваем это значение переменной
        # а также передает туда title, title попадает в kwargs, а из kwargs в context
        c_def = self.get_user_context(title="Главная страница")
        # объединяем c_def и context в один общий словарь
        context = dict(list(context.items()) + list(c_def.items()))
        return context

    # Этот методы выбирает только те значения из модели Women, у которых поле is_published = True
    # def get_queryset(self):
    #     return Women.objects.filter(is_published=True)


class WomenPost(DataMixin, ListView):
    model = Women
    template_name = 'ProStudy/category.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['posts'][0].cat - берем context, у него берем атрибут posts, выбираем оттуда
        # первую запись, и обращаемся к параметру cat, возвращаем название категории
        c_def = self.get_user_context(title='Категория - ' + str(context['posts'][0].cat),
                                      cat_selected=context['posts'][0].cat_id)
        # context['title'] = 'Категория - ' + str(context['posts'][0].cat)
        # context['menu'] = menu
        # Когда не существует никаких статей, выбранных через get_queryset, далее через фильтр
        # то возникает ошибка list index out of range, чтобы ее поправить, надо записать allow_empty = False
        # чтобы генерировалось исключение 404 СТРАНИЦА НЕ НАЙДЕНА
        context = dict(list(c_def.items()) + list(context.items()))
        return context

    def get_queryset(self):
        # cat__slug обращаемся к полю slug таблицы категорий cat
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'])


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'ProStudy/show_post.html'
    # По дефолту в urls для этот класс представления пытается взять записть по маршруту:
    # path('<slug:slug>/', ShowPost.as_view(), name='show_post'), но если я хочу оставить post_slug, то
    # нужно прописать специальную переменную slug_url_kwarg
    slug_url_kwarg = 'post_slug'
    # pk_url_kwarg - если используется id вместо slug'а
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        def_c = self.get_user_context(title='Статья о ' + str(context['posts'].title))
        # Отсюда беру только posts, в шаблоне перебираю post, у post беру cat и получаю Певицы или Актрисы
        # то есть получаю поле name из модели Categories
        context['cat_selected'] = context['posts'].cat
        context = dict(list(context.items()) + list(def_c.items()))
        return context

    def get_queryset(self):
        return Women.objects.all().select_related('cat')

# Класс представления для Форм
class AddPost(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'ProStudy/addpage.html'
    # Если не указана get_absolute_url в моделях
    success_url = reverse_lazy('home')
    # Адрес перенаправления для неавторизованных пользователей
    login_url = reverse_lazy('/home')
    # raise_exception = True - генерируется ошибка 403 (Доступ запрещен)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        def_c = self.get_user_context(title='Добавление поста')
        return dict(list(context.items()) + list(def_c.items()))


class AddCategory(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddCategoryForm
    template_name = 'ProStudy/add_cat.html'
    raise_exception = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        def_c = self.get_user_context(title='Добавление категории')
        return dict(list(context.items()) + list(def_c.items()))


class WomenCategories(DataMixin, ListView):
    model = Categories
    template_name = 'ProStudy/categories.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        def_c = self.get_user_context(title='Поиск по категориям')
        return dict(list(context.items()) + list(def_c.items()))


# Пагинация для функций-представления
def about(request):
    # Читаем список всех женщин
    contact_list = Women.objects.all()
    # Потом создаем пагинатор (3 элемента списка отобрадаются на странице)
    paginator = Paginator(contact_list, 3)
    # Получаем номер текущей страницы
    page_number = request.GET.get('page')
    # Формируем объект page_object, который будет содерожать список элементов текущей страницы
    page_obj = paginator.get_page(page_number)
    return render(request, 'ProStudy/base_page.html', {'page_obj': page_obj,'menu': menu, 'title': 'О сайте'})


# Регистраци пользователей реализована как форма, поэтому наследуем от CreateView
# А также в шаблоне сделаем как в форме
class RegisterUser(DataMixin, CreateView):
    # Стандартная форма для регистрации пользователей (можно использовать стандартную)
    # Но также можно сделать свою в forms.py для улучшения внешнего вида формы
    form_class = UserCreationForm
    template_name = 'ProStudy/register.html'
    # Перенапрвление на адрес пр успешной регистрации пользователя
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация пользователя')
        return dict(list(context.items()) + list(c_def.items()))

    # Автоматический входи при успешной регистрации
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('homepage')


# В класс LoginView реализована вся необходимая логика для авториции пользователя
class LoginUser(DataMixin, LoginView):
    # Стандартная форма для авторизации пользователя
    form_class = LoginUserForm
    template_name = 'ProStudy/login.html'

    def get_context_data(self, *, objects_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация пользователя")
        return dict(list(context.items()) + list(c_def.items()))

    # при успешной авторизации переходим на главную страницу
    # Но такую хрень можно сделть в setting.py, прописав константу LOGIN_REDIRECT_USL = '/'
    def get_success_url(self):
        return reverse_lazy('homepage')


# Наследуем от FormView, потому что не связываем с моделью
class ContactFormView(DataMixin, FormView):
    form_class = ContactForm
    template_name = 'ProStudy/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, list_object=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Обратная связь")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        print(form.cleaned_data)
        return redirect('homepage')


# Функция для выхода
def logout_user(request):
    logout(request)
    return redirect('login')



# def show_category(request, cat_slug):
#     # get_object_or_404 выбирает из таблицы Categories пост с первичным ключом, который передается
#     category = get_object_or_404(Categories, slug=cat_slug)
#
#     context = {
#         'cat_name': category.name,
#         'cat_description': category.short_description,
#         'cat_selected': category.id,
#     }
#
#     return render(request, 'ProStudy/category.html', context=context)
#
# def homepage(request): # В аргументах запрос (отрисовывает главную страницу по шаблону)
#     # return HttpResponse('код страницы')
#     # return render(request, '') request - httprequest, '' - путь к шаблону
#     context = {
#         'title': 'Онлайн-школа ProStudy',
#         'menu': menu,
#     }
#     return render(request, 'ProStudy/index.html', context=context)
# def add_page(request):
#
#     # # Создаем здесь экземпляр класса нашей формы
#     # # Затем эту штуку нужно записать в контекст
#     # form = AddPostForm()
#
#     # Верхняя штука - это по дефолту, если форма не отправилась, то ранее введенные данные не сохраняются
#     # Чтобф они сохранялись, нужно сделать проверку
#     # request.POST - all data user has entered in the form
#     # request.FILES - Для загрузки изображения (надо дописать в шаблоне в тэге form атрибут
#     # enctype="multipart/form-data")
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # print(form.cleaned_data)
#             # form.cleaned_data - это словарь с данными, которые приходят после отправки формы
#             # # Распаковываем словарь cleaned.data и передаем его методу create (Добавление в БД)
#             # # Но если форма связана с, то можно использовать form.save()
#             # Women.objects.create(**form.cleaned_data)
#             form.save()
#             return redirect('homepage')
#
#     else:
#         form = AddPostForm
#     context = {
#         'title': 'Добавить статью',
#         'menu': menu,
#         'form': form,
#     }
#     return render(request, 'ProStudy/addpage.html', context=context)
#
#
# def add_category(request):
#
#     if request.method == 'POST':
#         form = AddPostForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('homepage')
#     else:
#         form = AddCategoryForm
#
#     context = {
#         'title': 'Добавить категорию',
#         'menu': menu,
#         'form': form,
#     }
#     return render(request, 'ProStudy/add_cat.html', context=context)
#
#
# def programms(request):
#     context = {
#         'title': 'Программы',
#         'menu': menu,
#         # 'cats': categories,
#         # 'blocks': product_blocks,
#     }
#     return render(request, 'ProStudy/categories.html', context=context)
#
#
# def show_post(request, post_slug):
#     ps = get_object_or_404(Women, slug=post_slug)
#     context = {
#         'post_name': ps.title,
#         'post_id': ps.id,
#         'cat_selected': ps.cat,
#         'content': ps.content,
#     }
#     return render(request, 'ProStudy/show_post.html', context=context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')

