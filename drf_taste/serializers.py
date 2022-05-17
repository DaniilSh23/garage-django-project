from django.contrib.auth.models import User
from rest_framework import serializers
from drf_taste.models import Item


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'is_staff', 'username', 'email']


class ItemSerializer(serializers.Serializer):
    # текстовое поле максимум на 200 символов
    name = serializers.CharField(max_length=200)
    # необязательное для заполнения поле
    description = serializers.CharField(allow_blank=True)
    # вес не может быть меньше 0
    weight = serializers.FloatField(min_value=0)


class ItemModelSerializer(serializers.ModelSerializer):
    '''
    Класс для сериализации на основании модели
    '''
    class Meta:
        model = Item
        fields = ['id', 'name', 'description', 'weight']