# Generated by Django 4.0.4 on 2022-04-15 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0009_alter_comment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='user_name',
            field=models.CharField(db_index=True, max_length=100, verbose_name='Имя пользователя'),
        ),
    ]
