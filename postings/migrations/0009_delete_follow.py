# Generated by Django 4.0.3 on 2022-03-27 11:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('postings', '0008_follow'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Follow',
        ),
    ]
