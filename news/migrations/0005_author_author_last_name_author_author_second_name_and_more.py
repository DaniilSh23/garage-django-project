# Generated by Django 4.0.4 on 2022-04-13 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_author_authors_news_alter_news_author_news'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='author_last_name',
            field=models.CharField(blank=True, max_length=20, verbose_name='Фамилия автора'),
        ),
        migrations.AddField(
            model_name='author',
            name='author_second_name',
            field=models.CharField(blank=True, max_length=20, verbose_name='Отчество автора'),
        ),
        migrations.AddField(
            model_name='author',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
    ]