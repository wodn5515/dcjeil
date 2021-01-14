# Generated by Django 3.1.2 on 2021-01-14 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0006_auto_20201029_1244'),
        ('board', '0013_auto_20201224_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='div',
            field=models.ForeignKey(limit_choices_to={'m_type__contains': 'list'}, on_delete=django.db.models.deletion.CASCADE, related_name='post', to='menu.submenu', verbose_name='게시판'),
        ),
    ]
