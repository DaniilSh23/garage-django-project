from django.urls import path, include
from app_media.views import upload_file, translation_example
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('upload/', upload_file, name='upload_file'),
    # кэшируем эту страницу на 30 секунд
    path('trans_example/', cache_page(30)(translation_example), name='trans_example'),
    # в данной строке мы импортируем сразу все методы, используемые для локализации
    # среди них также находится метод set_language, который мы указали в шаблоне
    path('i18n', include('django.conf.urls.i18n')),
]