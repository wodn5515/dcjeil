# Generated by Django 3.1.2 on 2020-10-19 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0005_auto_20201019_2118'),
        ('board', '0005_auto_20201019_2011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='date',
            field=models.DateField(blank=True, help_text='필요시에만 작성하세요.<br>작성일이 아닙니다.', null=True, verbose_name='일시'),
        ),
        migrations.AlterField(
            model_name='post',
            name='div',
            field=models.ForeignKey(limit_choices_to={'m_type__contains': 'list'}, on_delete=django.db.models.deletion.CASCADE, to='menu.submenu', verbose_name='게시판'),
        ),
    ]
