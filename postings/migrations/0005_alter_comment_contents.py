# Generated by Django 4.0.3 on 2022-03-24 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('postings', '0004_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='contents',
            field=models.CharField(max_length=300, null=True),
        ),
    ]