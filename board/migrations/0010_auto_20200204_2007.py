# Generated by Django 2.1.15 on 2020-02-04 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0009_auto_20200204_1451'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='postimage',
            name='post',
        ),
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.TextField(blank=True, editable=False, verbose_name='사진'),
        ),
        migrations.DeleteModel(
            name='PostImage',
        ),
    ]
