# импорт модели, которой представлены пользователи системы аутентификации
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class News(models.Model):
    # список для параметра choices
    LIST_FOR_CHOICES = [
        ('p', 'published'),
        ('d', 'draft'),
        ('r', 'review')
    ]

    title = models.CharField(max_length=100, verbose_name=_('title'))
    content = models.TextField(max_length=4000, default='Описание отсутствует', verbose_name=_('description'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', db_index=True)
    update_at = models.DateTimeField(auto_now=True, verbose_name=_('date of change'))
    is_published = models.BooleanField(default=False, verbose_name=_('publication flag'))
    author_news = models.ManyToManyField('Author', default=None, blank=True, verbose_name=_('author'))
    # прописываем атрибут, в котором доступен будет виджет с вариантами выбора значения поля
    status = models.CharField(max_length=1, choices=LIST_FOR_CHOICES, default='r', verbose_name=_('news status'))
    slug = models.SlugField(db_index=True, max_length=25, default='slug')

    def __str__(self):
        return f'Заголовок новости: {self.title}'

    class Meta:
        db_table = 'Таблица новостей'
        ordering = ['-created_at']
        # название модели в ед. и мн. числе
        verbose_name = _('news')
        verbose_name_plural = _('news')
        # добавляем разрешение для публикации новости
        permissions = [
            ('permit', 'разрешение на публикацию'),
            ('testperm', 'тестовое разрешение'),
        ]


class FilesForNews(models.Model):
    file = models.FileField(upload_to=f'files/%Y/%m/%d', max_length=2000, null=True, blank=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        db_table = 'Таблица файлов для новостей'


class Comment(models.Model):
    user_name = models.CharField(max_length=100, verbose_name=_('user name'), db_index=True)
    comment_text = models.TextField(max_length=2000, verbose_name=_('comment text'))
    from_news = models.ForeignKey('News', on_delete=models.CASCADE, default=None, null=True, related_name='comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, related_name='user', blank=True)

    def __str__(self):
        return f'Комментарий пользователя: {self.user_name}'

    class Meta:
        db_table = 'Таблица комментариев'
        ordering = ['from_news']
        verbose_name = _('comment')
        verbose_name_plural = _('comments')


class Author(models.Model):
    author_name = models.CharField(max_length=20, verbose_name=_('authors name'), db_index=True)
    author_last_name = models.CharField(max_length=20, verbose_name=_('authors surname'), blank=True)
    author_second_name = models.CharField(max_length=20, verbose_name=_('authors second name'), blank=True)
    birthday = models.DateField(verbose_name=_('date of birth'), blank=True, null=True)
    biography = models.TextField(max_length=4000)
    # отношение МНОГИЕ-КО-МНОГИМ с моделью News
    authors_news = models.ManyToManyField(News, verbose_name=_('news'))

    def __str__(self):
        return f'Имя автора:{self.author_name}'

    class Meta:
        db_table = 'Таблица авторов'
        ordering = ['author_name']
        verbose_name = _('author')
        verbose_name_plural = _('authors')

