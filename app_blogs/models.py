from django.db import models


class Blog(models.Model):
    '''Модель блогов'''
    title = models.CharField(max_length=25)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        db_table = 'Таблица блогов'

    def __str__(self):
        return self.title


class BlogAuthor(models.Model):
    '''Модель авторов блога'''
    name = models.CharField(max_length=25)

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        db_table = 'Авторы блога'

    def __str__(self):
        return self.name


class BlogModerator(models.Model):
    '''Модератор блога'''
    name = models.CharField(max_length=25)

    class Meta:
        verbose_name = 'Модератор'
        verbose_name_plural = 'Модераторы'
        db_table = 'Модераторы блога'

    def __str__(self):
        return self.name


class BlogArticle(models.Model):
    '''Модель статей блога'''

    title = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    authors = models.ManyToManyField(BlogAuthor)
    moderator = models.ForeignKey(BlogModerator, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        db_table = 'Статьи блога'

    def __str__(self):
        return self.title


