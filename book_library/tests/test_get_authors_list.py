from django.test import TestCase
from book_library.models import LibraryBookAuthor


class TestGetAuthorsList(TestCase):
    num_authors = 100

    @classmethod
    def setUpTestData(cls, num_authors=num_authors):
        '''Наполняем БД записями об авторах для проведения теста'''

        for i_author in range(1, num_authors + 1):
            LibraryBookAuthor.objects.create(
                name=f'author № {i_author}',
                surname=f'surname #{i_author}',
                birth_year=1000 + i_author)

    def test_get_authors_list(self):
        '''Тестовый метод получения списка авторов'''

        response = self.client.get('/book_lib/authors_list/')
        self.assertEqual(response.status_code, 200)

