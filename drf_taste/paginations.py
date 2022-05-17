from rest_framework.pagination import PageNumberPagination


class LargeResultsSetPagination(PageNumberPagination):
    '''
    Класс - пагинатор для отображения большого количества записей.
    page_size - размер страницы (количество записей БД, выводимых на страницу)
    page_size_query_param - параметр, к которому привязываемся для пагинации
    max_page_size - максимальный размер страницы
    '''

    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

class StandardResultsSetPagination(PageNumberPagination):
    '''
    Класс - пагинатор для отображения стандартного количества записей.
    page_size - размер страницы (количество записей БД, выводимых на страницу)
    page_size_query_param - параметр, к которому привязываемся для пагинации
    max_page_size - максимальный размер страницы
    '''

    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000