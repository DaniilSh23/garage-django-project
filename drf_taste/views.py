from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_taste.models import Item
from drf_taste.paginations import StandardResultsSetPagination
from drf_taste.serializers import ItemSerializer, ItemModelSerializer


def items_list(request):
    if request.method == 'GET':
        items_for_sale = [
            Item(
                name='Кофеварка',
                description='Варит отличный кофе',
                weight=100
            ),
            Item(
                name='Беспроводные наушники',
                description='Отличный звук',
                weight=150
            ),
        ]
        # JsonResponse сериализует данные, которые переданы в качестве аргумента, в формат JSON
        # прогоняем каждый инстанс класса Item через метод to_dict
        # берём класс-сериалайзер, прописанный ранее в serializers.py
        # закидываем в него список из инстансов класса Item
        # параметр many=True говорит сериалайзеру, что обрабатывать нужно список
        # когда мы получаем объект data сериалайзера, объекты Item будут
        # преобразованы в собственные типы данных Питона, в нашем случае - в словари
        return JsonResponse(ItemSerializer(items_for_sale, many=True).data, safe=False)


class ItemsModelList(APIView):
    '''
    Представление с использование APIView и СЕРИАЛИЗАТОРА
    По GET - запросу отправляет клиенту информацию о всех записях в ТБД Item
    POST - запрос: создаёт в ТБД Item новую запись и отправляет
    статус-код с уведомлением о результатах запроса
    '''

    def get(self, request):
        items = Item.objects.all()
        serializer = ItemModelSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        print(f'Данные запроса {request.data}')
        # данные запроса передадим в сериалайзер для модели
        serializer = ItemModelSerializer(data=request.data)
        print(f'Сериалайзер {serializer}')
        # проверим валидность входных данных
        if serializer.is_valid():
            # вызовем метод save(), который создаст новую запись в БД и вернёт ответ
            serializer.save()
            # отдаём ответ. Этот метод респонс от ДРФ типо круче, чем другой,
            # потому что высчитывает свой конечный результат в процессе ответа,
            # хз зачем мне эта инфа, если ниче не понятно
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class ItemsModelListMixin(ListModelMixin, CreateModelMixin, GenericAPIView):
    '''
    Представление с использованием МИКСИНОВ
    GenericAPIView - реализует базовый функционал
    ListModelMixin - (миксин) предоставляет метод list (просмотр)
    CreateModelMixin - (миксин) предоставляет метод create (создание)


    queryset - используется для того, чтобы возвращать объекты представления
    serializer_class - используется для валидации: сериализации ввода и сериализации вывода

    GET - запрос: отдаём данные из БД
    POST - запрос: вносим новую строку в БД
    '''

    # queryset используется для того, чтобы возвращать объекты представления
    queryset = Item.objects.all()
    # используется для валидации: сериализации ввода и сериализации вывода
    serializer_class = ItemModelSerializer

    def get(self, request):
        # явно привязываем метод list к нужному запросу
        return self.list(request)

    def post(self, request, format=None):
        # явно привязываем метод create к нужному запросу
        return self.create(request)


class ItemsModelListMixinVol2(ListModelMixin, CreateModelMixin, GenericAPIView):
    '''
    Представление с использованием МИКСИНОВ
    GenericAPIView - реализует базовый функционал
    ListModelMixin - (миксин) предоставляет метод list (просмотр)
    CreateModelMixin - (миксин) предоставляет метод create (создание)

    serializer_class - используется для валидации: сериализации ввода и сериализации вывода
    pagination_class - выбор нашего класса для пагинации

    get_queryset - переопределяем метод get_queryset для отбора нужных нам данных

    GET - запрос: отдаём данные из БД
    POST - запрос: вносим новую строку в БД
    '''

    # используется для валидации: сериализации ввода и сериализации вывода
    serializer_class = ItemModelSerializer
    # выбор класса-пагинатора
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        '''
        Переопределённый метод из GenericAPIView для отбора нужных нам данных
        '''

        # берём все данные из таблицы БД
        queryset = Item.objects.all()
        # берём данные по ключу name из запроса пользователя
        item_name = self.request.query_params.get('name')
        # проверяем есть ли данные по такому ключу в запросе пользователя
        if item_name:
            # отбираем те записи БД, у которых поле name == значению из запроса пользователя
            queryset = queryset.filter(name=item_name)
        # отдаём последовательность
        # если ключа name не будет в запросе пользователя, то вернутся все записи из ТБД
        # ВАЖНО: ключ МОЖЕТ БЫТЬ передан, но со значением, которого нет в БД и тогда вернётся пустой список
        return queryset

    def get(self, request):
        # явно привязываем метод list к нужному запросу
        return self.list(request)

    def post(self, request, format=None):
        # явно привязываем метод create к нужному запросу
        return self.create(request)