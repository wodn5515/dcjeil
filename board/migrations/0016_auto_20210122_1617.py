# Generated by Django 3.1.2 on 2021-01-22 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0015_auto_20210122_1515'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(verbose_name='내용'),
        ),
    ]
