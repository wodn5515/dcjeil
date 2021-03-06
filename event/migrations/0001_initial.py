# Generated by Django 3.1.2 on 2020-12-27 21:36

from django.db import migrations, models
import event.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewYearEveWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=5, verbose_name='이름')),
                ('parish', models.CharField(choices=[('1', '1교구'), ('2', '2교구'), ('3', '3교구'), ('4', '1청년부'), ('5', '2청년부'), ('6', '3청년부'), ('7', '주일학교')], max_length=10, verbose_name='교구')),
                ('words', models.ImageField(upload_to=event.models.new_year_eve_word_upload, verbose_name='말씀')),
            ],
        ),
    ]
