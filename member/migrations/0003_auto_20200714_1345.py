# Generated by Django 2.1.15 on 2020-07-14 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_auto_20200708_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='name',
            field=models.CharField(default='', max_length=5, verbose_name='이름'),
        ),
        migrations.AlterField(
            model_name='user',
            name='uid',
            field=models.CharField(error_messages={'unique': '이미 가입된 아이디 입니다.'}, max_length=50, unique=True, verbose_name='ID'),
        ),
    ]
