# Generated by Django 2.1.15 on 2020-01-22 20:27

import data.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0014_community_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='community',
            name='image',
            field=models.ImageField(blank=True, upload_to=data.models.community_image_save, verbose_name='사진'),
        ),
    ]
