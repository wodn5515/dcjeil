# Generated by Django 3.1.2 on 2020-12-23 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0008_auto_20201223_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_reserved',
            field=models.BooleanField(default=False, verbose_name='예약게시글'),
        ),
    ]
