from django.db import models


class LibraryBookAuthor(models.Model):
    '''Модель автор книги из библиотеки'''

    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=25, blank=True)
    birth_year = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Авторы книг библиотеки'


class LibraryBook(models.Model):
    '''Модель книга из библиотеки'''

    title = models.CharField(max_length=1000)
    isbn_standard = models.CharField(max_length=1000)
    year_of_issue = models.IntegerField()
    number_of_pages = models.IntegerField()
    authors_name = models.ForeignKey(LibraryBookAuthor, on_delete=models.CASCADE, default=None, null=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'Книги библиотеки'
