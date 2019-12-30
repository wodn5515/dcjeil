from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_delete
from django.dispatch import receiver
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
from imagekit.utils import get_cache
from random import choice
from account.models import User as account
import string

def post_video_save(instance, filename):
    extension = filename.split('.')[-1]
    return f'{instance.title}/file/video.extention'

def post_audio_save(instance, filename):
    extension = filename.split('.')[-1]
    return f'{instance.title}/file/audio.{extension}'

'''--------------------------- Abandoned ----------------------------'''

def post_image_save(instance, filename):
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr)
    extension = filename.split('.')[-1]
    return f'{instance.post.title}/image/{pid}.{extension}'

def set_defautwriter_when_deleted():
    return account.objects.get(is_superuser=True)

# Create your models here.
class Post(models.Model):
    
    class Meta:
        verbose_name = ('게시글')
        verbose_name_plural = ('게시글 관리')

    Divs = (
        ('201','금주의 말씀'), ('202','주일오후예배'), ('203','수요예배'),
        ('204','금요철야예배'), ('205','새벽기도'), ('206','부흥회'),
        ('301','할렐루야 찬양대'), ('302','호산나 찬양대'), ('303','찬양, 간증 집회'),
        ('401','공지사항'), ('402','교회소식'), ('403','교우소식'), ('404','새가족소개'),
        ('405','교회앨범'), ('406','자유게시판'), ('407','기도요청'), ('408','행사동영상'), ('409','큐티나눔방'),
        ('601','선교위원회'),('602','국내선교'),('603','캄보디아'),('604','인도'),('605','일본'),('606','태국'),
        ('607','필리핀'),('608','이집트'),('609','탄자니아'),('610','카메룬'),('611','남아공'),('612','러시아'),
        ('613','볼리비아'),('614','파푸아뉴기니'),('615','헝가리'),('616','단기선교'),
        ('702','새가족부 자료실'), ('703','확신반 자료실'),
        ('801','문서자료실'), ('802','기타자료실'), ('803','주보자료실'),
    )
    div = models.CharField(_("분류"), max_length=10, choices=Divs)
    upload_date = models.DateTimeField(_('등록일'), default=timezone.now)
    title = models.CharField(_('제목'), max_length=50, blank=True)
    preacher = models.CharField(_('설교자'), max_length=20, blank=True)
    writer = models.ForeignKey(account, on_delete=models.SET(set_defautwriter_when_deleted), related_name='post')
    video = models.CharField(_('동영상'), max_length=255, blank=True)
    words = models.CharField(_('오늘의 말씀'), max_length=50, blank=True)
    content = models.TextField(_('내용'), blank=True)
    views = models.IntegerField(_('조회수'), default=0)
    published = models.BooleanField(_('공개여부'), default=True)

    def __str__(self):
        return f'{self.get_div_display()} / {self.title}'

    @property
    def viewsup(self):
        self.views += 1
        self.save()

class PostImage(models.Model):

    class Meta:
        verbose_name = ('사진')
        verbose_name_plural = ('사진')

    post = models.ForeignKey(Post, on_delete=models.CASCADE, default='', verbose_name='게시글', related_name='image')
    image = models.ImageField(_('사진'), upload_to=post_image_save)
    desc = models.TextField(_('설명'), blank=True)
    thumbnail = ImageSpecField(
        source='image',
        processors=[Thumbnail(200,150)],
        format = 'JPEG',
        options = {'quality':200}
    )

    def __str__(self):
        temp = self.image.name.split('/')[-1]
        return f'{self.post.title} - {temp}'

class Comment(models.Model):

    class Meta:
        verbose_name = ('댓글')
        verbose_name_plural = ('댓글')

    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='게시글', related_name='comment')
    writer = models.ForeignKey(account, on_delete=models.CASCADE, verbose_name='작성자', related_name='writer')
    content = models.TextField(_('내용'), blank=True)
    date = models.DateTimeField(_('등록일'), default=timezone.now)

    def __str__(self):
        return f'{self.post.title} - {self.writer}'

class FixedView(models.Model):

    class Meta:
        verbose_name = ('고정 템플릿 관리')
        verbose_name_plural = ('고정 템플릿 관리')

    Menu = (
        ('101','인사말'),('102','교회연혁'),('103','우리의 비젼'),
        ('104','담임목사소개'),('105','섬기는 사람들'),('106','찾아오시는 길'),
        ('207','예배안내'),('501','영아부'),('502','유치부'),('503','유년부'),
        ('504','초등부'),('505','중등부'),('506','고등부'),('507','사랑부'),
        ('508','청년1부'),('509','청년2부'),('510','청년3부'),('511','어린이집'),
        ('701','양육시스템')
    )

    div = models.CharField(_("분류"), max_length=10, choices=Menu)
    html = models.TextField(_("html"), blank=False)

    def __str__(self):
        return f'{self.get_div_display()}'