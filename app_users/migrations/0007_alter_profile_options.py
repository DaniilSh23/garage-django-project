# Generated by Django 4.0.4 on 2022-04-17 11:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0006_alter_profile_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'ordering': ['news_counter'], 'permissions': (('verificate', 'Верификация'),)},
        ),
    ]
