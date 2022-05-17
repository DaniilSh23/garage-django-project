from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin

from book_library.filters import FilterBooksByPages, FilterAuthorsByName
from book_library.models import LibraryBook, LibraryBookAuthor
from book_library.serializers import BooksListModelSerializer, BookAuthorListModelSerializer


class GetBooksList(ListModelMixin, GenericAPIView):
    '''Класс-представление для работы с моделью LibraryBook'''

    queryset = LibraryBook.objects.all()
    serializer_class = BooksListModelSerializer

    def get(self, request):
        return self.list(request)


class GetAuthorsList(ListModelMixin, GenericAPIView):
    '''Класс-представление для работы с моделью LibraryBookAuthor'''

    queryset = LibraryBookAuthor.objects.all()
    serializer_class = BookAuthorListModelSerializer

    def get(self, request):
        return self.list(request)


class FilterBooksList(ListModelMixin, GenericAPIView):
    '''Класс-представление для фильтрации вывода списка книг по автору и названию'''

    serializer_class = BooksListModelSerializer
    # установка бэкэнд фильтра по умолчанию
    filter_backends = (DjangoFilterBackend,)
    # выбор класса-фильтра (прописан вручную в filters.py)
    filter_class = FilterBooksByPages

    def get_queryset(self):
        '''Переопределённый метод из GenericAPIView для получение нужных нам данных'''

        queryset = LibraryBook.objects.all()
        authors_name = self.request.query_params.get('author')
        books_title = self.request.query_params.get('title')

        if authors_name and books_title:
            queryset = queryset.filter(title=books_title, authors_name=authors_name)

        return queryset

    def get(self, request):
        return self.list(request)


class FilterAuthorsListByName(ListModelMixin, GenericAPIView):
    '''Класс-представление для фильтрации вывода авторов по имени'''

    queryset = LibraryBookAuthor.objects.all()
    serializer_class = BookAuthorListModelSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = FilterAuthorsByName

    def get(self, request):
        return self.list(request)


class BooksDetail(UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericAPIView):
    '''
    Представление для получения детальной информации о книге,
    а также реализующее методы удаления и изменения записей о книгах.
    '''

    queryset = LibraryBook.objects.all()
    serializer_class = BooksListModelSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


