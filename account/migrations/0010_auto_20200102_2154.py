# Generated by Django 2.1.15 on 2020-01-02 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20200102_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birthday',
            field=models.CharField(max_length=10, verbose_name='생년월일'),
        ),
    ]
