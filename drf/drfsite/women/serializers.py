from rest_framework import serializers
from .models import *


class WomenSerializer(serializers.ModelSerializer):
    # Указываем пользователя по умолчанию (удалится выбор id пользователя при добавлении поста)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Women
        # Можно указать поле cat, которое вернет id категории
        fields = "__all__"






# # Создаем класс сериализатора, наследуя его от сериализатора, который рабртает с моделями
# class WomenSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=255)
#     # В модели это TextField, но для сериализатора используем CharField, который формирует строку
#     # потому что в в сериализаторе будет формироавться байтовая json-строка
#     content = serializers.CharField()
#     # Они формируются автоматически, поэтому пропишем, что эти поля только для чтения с помощью
#     # read_only = True
#     time_create = serializers.DateTimeField(read_only=True)
#     time_updated = serializers.DateTimeField(read_only=True)
#     is_published = serializers.BooleanField(default=True)
#     # В модели это поле объявлено как Foreign Key, но при формировании json-строки
#     # это поле будет в виде целого числа (номера категории), поэтому IntegerField
#     cat_id = serializers.IntegerField()
#
#     # Метод create() - добавление записи в БД
#     # validated_data - словарь проверенных данных, которые пришли с POST-запросом
#     # Он формируется во views в методе post в методе is_valid(
#     def create(self, validated_data):
#         return Women.objects.create(**validated_data)
#
#     # instance - это ссылка на объект модели Women
#     # validated_data - словарь из проверенных данных, который нужно изменить в БД
#     def update(self, instance, validated_data):
#         # Берем поле из модели instance и присваиваем ему нужное значение
#         # Если мы не можем с помощью метода get взять title, то передадим уже заданное значение
#         instance.title = validated_data.get("title", instance.title)
#         instance.content = validated_data.get("content", instance.content)
#         instance.time_updated = validated_data.get("time_updated", instance.time_updated)
#         instance.is_published = validated_data.get("is_published", instance.is_published)
#         instance.cat_id = validated_data.get("cat_id", instance.cat_id)
#         # Сохраняем
#         instance.save()
#         # Возвращаем наш объект
#         return instance

