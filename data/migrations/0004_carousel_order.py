# Generated by Django 2.1.15 on 2020-01-18 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_carousel_server'),
    ]

    operations = [
        migrations.AddField(
            model_name='carousel',
            name='order',
            field=models.IntegerField(default=0, help_text='낮을수록 먼저나옵니다.', verbose_name='순서'),
        ),
    ]
