# Generated by Django 4.0.4 on 2022-04-12 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('content', models.TextField(default='Описание отсутствует', max_length=4000, verbose_name='Описание')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата создания')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Дата изменения')),
                ('is_published', models.BooleanField(default=False, verbose_name='Флаг публикации')),
            ],
            options={
                'db_table': 'Hot news Gotham City',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(db_index=True, max_length=100, verbose_name='Имя пользователя')),
                ('comment_text', models.TextField(max_length=2000, verbose_name='Текст комментария')),
                ('from_news', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comment', to='news.news')),
            ],
            options={
                'db_table': 'Who is Batman?',
                'ordering': ['from_news'],
            },
        ),
    ]
