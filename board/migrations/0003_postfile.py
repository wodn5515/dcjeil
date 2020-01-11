# Generated by Django 2.1.15 on 2020-01-01 11:54

import board.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0002_postimage_desc'),
    ]

    operations = [
        migrations.CreateModel(
            name='PostFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=board.models.post_file_save, verbose_name='첨부파일')),
                ('post', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='file', to='board.Post', verbose_name='게시글')),
            ],
            options={
                'verbose_name': '첨부파일',
                'verbose_name_plural': '첨부파일',
            },
        ),
    ]