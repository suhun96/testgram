# Generated by Django 4.0.3 on 2022-03-24 06:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postings', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='image',
            old_name='Img',
            new_name='img',
        ),
    ]
