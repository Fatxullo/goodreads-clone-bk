# Generated by Django 4.2.4 on 2023-08-13 12:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_book_cover_book'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='cover_book',
            new_name='cover_picture',
        ),
    ]
