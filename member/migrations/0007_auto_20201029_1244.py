# Generated by Django 3.1.2 on 2020-10-29 12:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0008_carousel_link'),
        ('member', '0006_auto_20201020_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='duty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='data.duty', verbose_name='직분'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_registered',
            field=models.BooleanField(default=False, help_text='◈ 본 교회 교인이시면 체크해주세요.', verbose_name='교인여부'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=False, help_text='◈ 관리자페이지 접속권한', verbose_name='스태프'),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, help_text='◈ 최고등급의 관리자권한', verbose_name='관리자'),
        ),
        migrations.AlterField(
            model_name='user',
            name='tp',
            field=models.CharField(error_messages={'unique': '이미 가입된 연락처입니다.'}, help_text="◈ ' - '를 제외하고 입력해주세요.", max_length=15, null=True, unique=True, verbose_name='연락처'),
        ),
    ]
