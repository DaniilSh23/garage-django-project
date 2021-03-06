# Generated by Django 4.0.4 on 2022-04-23 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0023_alter_filesfornews_file_alter_filesfornews_news'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='author',
            options={'ordering': ['author_name'], 'verbose_name': 'author', 'verbose_name_plural': 'authors'},
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['from_news'], 'verbose_name': 'comment', 'verbose_name_plural': 'comments'},
        ),
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ['-created_at'], 'permissions': [('permit', 'разрешение на публикацию'), ('testperm', 'тестовое разрешение')], 'verbose_name': 'news', 'verbose_name_plural': 'news'},
        ),
        migrations.AlterField(
            model_name='author',
            name='author_last_name',
            field=models.CharField(blank=True, max_length=20, verbose_name='authors surname'),
        ),
        migrations.AlterField(
            model_name='author',
            name='author_name',
            field=models.CharField(db_index=True, max_length=20, verbose_name='authors name'),
        ),
        migrations.AlterField(
            model_name='author',
            name='author_second_name',
            field=models.CharField(blank=True, max_length=20, verbose_name='authors second name'),
        ),
        migrations.AlterField(
            model_name='author',
            name='authors_news',
            field=models.ManyToManyField(to='news.news', verbose_name='news'),
        ),
        migrations.AlterField(
            model_name='author',
            name='birthday',
            field=models.DateField(blank=True, null=True, verbose_name='date of birth'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_text',
            field=models.TextField(max_length=2000, verbose_name='comment text'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user_name',
            field=models.CharField(db_index=True, max_length=100, verbose_name='user name'),
        ),
        migrations.AlterField(
            model_name='news',
            name='author_news',
            field=models.ManyToManyField(blank=True, default=None, to='news.author', verbose_name='author'),
        ),
        migrations.AlterField(
            model_name='news',
            name='content',
            field=models.TextField(default='Описание отсутствует', max_length=4000, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='news',
            name='is_published',
            field=models.BooleanField(default=False, verbose_name='publication flag'),
        ),
        migrations.AlterField(
            model_name='news',
            name='status',
            field=models.CharField(choices=[('p', 'published'), ('d', 'draft'), ('r', 'review')], default='r', max_length=1, verbose_name='news status'),
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=100, verbose_name='title'),
        ),
        migrations.AlterField(
            model_name='news',
            name='update_at',
            field=models.DateTimeField(auto_now=True, verbose_name='date of change'),
        ),
    ]
