# Generated by Django 2.1.2 on 2019-09-20 12:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20190918_1344'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='group',
            new_name='office',
        ),
    ]
