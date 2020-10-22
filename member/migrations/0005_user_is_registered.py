# Generated by Django 3.1.2 on 2020-10-20 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0004_auto_20201020_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_registered',
            field=models.BooleanField(default=False, help_text='본 교회 교인만 체크해주세요.', verbose_name='교인여부'),
        ),
    ]