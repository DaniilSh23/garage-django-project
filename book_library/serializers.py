from rest_framework import serializers
from book_library.models import LibraryBook, LibraryBookAuthor


class BooksListModelSerializer(serializers.ModelSerializer):
    '''Класс-сериалайзер для модели LibraryBook'''

    class Meta:
        model = LibraryBook
        fields = ['title', 'isbn_standard', 'year_of_issue', 'number_of_pages', 'authors_name', 'id']


class BookAuthorListModelSerializer(serializers.ModelSerializer):
    '''Класс-сериалайзер для модели LibraryBookAuthor'''

    class Meta:
        model = LibraryBookAuthor
        fields = ['name', 'surname', 'birth_year', 'id']

