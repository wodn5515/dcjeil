# Generated by Django 3.1.2 on 2020-10-19 20:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0003_auto_20201015_1615'),
        ('board', '0002_auto_20201018_1142'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='menu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='menu.submenu', verbose_name='게시판'),
        ),
        migrations.AlterField(
            model_name='post',
            name='div',
            field=models.CharField(choices=[('201', '금주의 말씀'), ('202', '주일오후예배'), ('203', '수요예배'), ('204', '금요철야예배'), ('205', '새벽기도'), ('206', '부흥회'), ('301', '할렐루야 찬양대'), ('302', '호산나 찬양대'), ('303', '찬양, 간증 집회'), ('401', '공지사항'), ('402', '교회소식'), ('403', '새가족소개'), ('404', '교회앨범'), ('405', '자유게시판'), ('406', '기도요청'), ('407', '행사동영상'), ('408', '큐티나눔방'), ('601', '선교위원회'), ('602', '국내선교'), ('603', '아시아'), ('604', '아프리카'), ('605', '기타'), ('606', '단기선교'), ('702', '새가족부 자료실'), ('703', '확신반 자료실'), ('801', '문서자료실'), ('802', '기타자료실'), ('803', '주보자료실')], max_length=10, verbose_name='분류'),
        ),
    ]