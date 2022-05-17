from django.test import TestCase
from book_library.models import LibraryBook, LibraryBookAuthor


class TestGetBooksList(TestCase):
    num_books = 100
    num_authors = 2

    @classmethod
    def setUpTestData(cls, num_books=num_books, num_authors=num_authors):
        '''Наполняем БД записями о книгах для проведения теста'''

        for i_author in range(1, num_authors + 1):
            LibraryBookAuthor.objects.create(
                name=f'author № {i_author}',
                surname=f'surname #{i_author}',
                birth_year=1000 + i_author)

        for i_book in range(1, num_books + 1):
            if i_book % 2 == 0:
                authors_name = LibraryBookAuthor.objects.get(name='author № 2')
            elif i_book % 2 != 0:
                authors_name = LibraryBookAuthor.objects.get(name='author № 1')
            LibraryBook.objects.create(
                title=f'Название книги №{i_book}',
                isbn_standard=f'{i_book}-{i_book}-{i_book}-{i_book}',
                year_of_issue=(2000 - i_book),
                number_of_pages=(100 + i_book),
                authors_name=authors_name
            )

    def test_get_books_list(self):
        '''Тестовый запрос к БД для получения списка книг'''

        response = self.client.get('/book_lib/books_list/')
        self.assertEqual(response.status_code, 200)






