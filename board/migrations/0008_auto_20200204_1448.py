# Generated by Django 2.1.15 on 2020-02-04 14:48

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0007_auto_20200130_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=ckeditor_uploader.fields.RichTextUploadingField(error_messages={'blank': '내용을 입력해주세요.', 'null': '내용을 입력해주세요.'}, verbose_name='내용'),
        ),
    ]