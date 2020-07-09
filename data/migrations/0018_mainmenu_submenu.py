# Generated by Django 2.1.15 on 2020-06-10 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0017_auto_20200211_1640'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mainmenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='메뉴명')),
                ('order', models.IntegerField(help_text='낮을수록 먼저 배치됩니다', unique=True, verbose_name='순서')),
            ],
            options={
                'verbose_name': '메인메뉴 관리',
                'verbose_name_plural': '메인메뉴 관리',
            },
        ),
        migrations.CreateModel(
            name='Submenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='메뉴명')),
                ('order', models.IntegerField(help_text='낮을수록 먼저 배치됩니다', verbose_name='순서')),
                ('mainmenu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submenu', to='data.Mainmenu', verbose_name='메인메뉴')),
            ],
            options={
                'verbose_name': '서브메뉴 관리',
                'verbose_name_plural': '서브메뉴 관리',
            },
        ),
    ]