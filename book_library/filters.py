import django_filters
from book_library.models import LibraryBook, LibraryBookAuthor


class FilterBooksByPages(django_filters.FilterSet):
    '''Класс фильтрации списка книг по имени автора, числу страниц'''

    class Meta:
        model = LibraryBook
        fields = {
            'number_of_pages': ['gte', 'lte', 'exact'],
            'authors_name': ['exact'],
        }


class FilterAuthorsByName(django_filters.FilterSet):
    '''Класс фильтрации списка авторов по имени'''

    class Meta:
        model = LibraryBookAuthor
        fields = {
            'name': ['icontains']   # примерное совпадение без учёта регистра
        }


def sum_numbers(a: float, b: float) -> float:
    """
    Складываем два числа.
    :param a: Первое слагаемое
    :type a: float
    :param b: Второе слагаемое
    :type b: float, int
    :return: Сумма
    :rtype: float
    """
    return a + b
