# Generated by Django 3.1.2 on 2020-12-24 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0009_post_is_reserved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='reservation',
        ),
    ]
