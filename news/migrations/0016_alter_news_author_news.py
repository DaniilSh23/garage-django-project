# Generated by Django 4.0.4 on 2022-04-17 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0015_alter_news_author_news'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='author_news',
            field=models.ManyToManyField(blank=True, default=None, to='news.author', verbose_name='Автор'),
        ),
    ]
