# Generated by Django 3.1.2 on 2020-10-15 16:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_auto_20201015_1614'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submenu',
            name='tag',
        ),
        migrations.RemoveField(
            model_name='submenu',
            name='using_tag',
        ),
    ]
