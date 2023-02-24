from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly

from .models import *
from .serializers import WomenSerializer
from rest_framework.views import APIView


class WomenAPIList(generics.ListCreateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    # Прописываем права доступа
    permission_classes = (IsAuthenticatedOrReadOnly, )


class TokenAuthentificated:
    pass


class WomenAPIUpdate(generics.RetrieveUpdateAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    permission_classes = (IsOwnerOrReadOnly, IsAuthenticated)
    # В отдельности прописываем авторизацию по только токену для этой вьюшки
    authentication_classes = (TokenAuthentificated, )


class WomenAPIDestroy(generics.RetrieveDestroyAPIView):
    queryset = Women.objects.all()
    serializer_class = WomenSerializer
    # Такие права дают доступ только админам сайта
    permission_classes = (IsAdminOrReadOnly, )





# # определили ViewSet
# class WomenViewSet(viewsets.ModelViewSet):
#     # Ссылается на список записей, возвращаемых клиенту
#     # Если мы его убираем, то при регистрации роутера нужно прописать basename
#     queryset = Women.objects.all()
#     # Сериалайзер, который мы будем применять к этому queryset
#     serializer_class = WomenSerializer
#
#     # Вернуть определенные записи из БД
#     def get_queryset(self):
#         # Получаем pk
#         pk = self.kwargs.get("pk")
#         if not pk:
#             return Women.objects.all()[:4]
#
#         return Women.objects.filter(pk=pk)
#
#     # Пишем свой роутер
#     @action(methods=['get'], detail=True) # detail = True - одна запись, False - список записей
#     # Когда читаем запись, то дополнительно вводим параметр pk
#     def category(self, request, pk=None):
#         cats = Category.objects.get(pk=pk)
#         # return Response({'cats': [cat.name for cat in cats]})
#         return Response({'cats': cats.name})


# # наследуем от класс для чтения (GET-запроса) и создания (POST-запроса)
# class WomenAPIList(generics.ListCreateAPIView):
#     # Ссылается на список записей, возвращаемых клиенту
#     queryset = Women.objects.all()
#     # Сериалайзер, который мы будем применять к этому queryset
#     serializer_class = WomenSerializer
#
#
# # Наследуется от класса, который позволяет выполнять PUT-запросы
# # позволяет обновить (изменить) запись в БД (put и patch запросы)
# class WomenAPIUpdate(generics.UpdateAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer
#
#
# # Наследуем от класса, который дает доступ к CRUD-операциям
# class WomenAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Women.objects.all()
#     serializer_class = WomenSerializer

# # APIView - самый базовый класс, от которого наследуются все остальные классы прдеставления DRF
# class WomenAPIView(APIView):
#     # Метод get будет выполняться, когда будет поступать get-запрос со стороны пользователя
#     # Парметр request содерить все параметры входящего get-запроса
#     def get(self, request):
#         # С помощью класса Responce будем возвращшать клиенту json-строку
#         # Словарь автоматически будет преобразован в json-строку с помощью класса Responce
#         # Women.objects.all() дает qeryset, чтобы получить все значения, нужно применить метод values()
#         # lst = Women.objects.all().values()
#         # return Response({'posts': list(lst)})
#         w = Women.objects.all()
#         # Указываем many = True, потому что изначально он False, а работать будет с множеством записей
#         return Response({'posts': WomenSerializer(w, many=True).data})
#
#     # Автоматически базовый класс APIView не разрешает POST-запросы, поэтому прописываем метод post
#     def post(self, request):
#         # Создаем сериализатор, на основе тех данных, которые поступили с post-запросом (request.data)
#         serializer = WomenSerializer(data=request.data)
#         # Проверяем корректность принятых данных (здесь формируется словарь validated_data)
#         serializer.is_valid(raise_exception=True)
#         # Метод save() автоматически вызовект метод create из WomenSerializer
#         serializer.save()
#         # # Добавляем в БД с помощью метода create, в скобках указываем параметры для записи в таблицу
#         # # После определния метода create у сериализатора строчки ниже можно закомментровать
#         # # и замень на serializer.save()
#         # post_new = Women.objects.create(
#         #     title=request.data['title'],
#         #     content=request.data['content'],
#         #     cat_id=request.data['cat_id']
#         # )
#
#         # model_to_dict - стандартная Django-функция, преобразует моедль в словарь
#         # return Response({'post': model_to_dict(post_new)})
#         # return Response({'post': WomenSerializer(post_new).data}) - это без метода save
#         return Response({'post': serializer.data}) # С методом save()
#         # data будет ссылаться на новый созданный объект
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({"error": "Method PUT not allowed"})
#
#         try:
#             instance = Women.objects.get(pk=pk)
#         except:
#             return Response({"error": "Object does not exists"})
#
#         # request.data - Это те данные, которые нам нужно изменить
#         # instance = instance - Тот объект (запись), который будем менять
#         serializer = WomenSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         # Метод save() автоматически вызовет метод update
#         serializer.save()
#         return Response({"post": serializer.data})
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk", None)
#         if not pk:
#             return Response({'post': 'Method DELETE is not allowed'})
#
#         try:
#             Women.objects.get(pk=pk)
#         except:
#             return Response({"error": "Object does not exists"})
#
#         Women.objects.filter(pk=pk).delete()
#
#         return Response({"post": "deleted post " + str(pk)})
#
# #
# # # Создаем класс представления, который наследуем от специального класса
# # class WomenAPIView(generics.ListAPIView):
# #     queryset = Women.objects.all()
# #     # Сюда указываем класс сериализатор
# #     serializer_class = WomenSerializer
