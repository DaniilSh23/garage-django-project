# Generated by Django 4.0.4 on 2022-04-26 07:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book_library', '0002_alter_librarybook_table_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='librarybook',
            name='authors_name',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='book_library.librarybookauthor'),
        ),
    ]
