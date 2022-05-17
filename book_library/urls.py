from django.urls import path
from book_library.views import GetBooksList, GetAuthorsList, FilterBooksList, FilterAuthorsListByName, BooksDetail

urlpatterns = [
    path('books_list/', GetBooksList.as_view(), name='books_list'),
    path('authors_list/', GetAuthorsList.as_view(), name='authors_list'),
    path('filter_books/', FilterBooksList.as_view(), name='filter_books'),
    path('filter_authors/', FilterAuthorsListByName.as_view(), name='filter_authors'),
    path('books_list/<int:pk>/', BooksDetail.as_view(), name='book_detail'),
]