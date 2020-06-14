from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_delete
from django.dispatch import receiver
from ckeditor_uploader.fields import RichTextUploadingField
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
from imagekit.utils import get_cache
from random import choice
from account.models import User as account
import string

'''--------------------------- Abandoned ----------------------------'''

def post_video_save(instance, filename):
    extension = filename.split('.')[-1]
    return f'{instance.title}/file/video.extention'

def post_audio_save(instance, filename):
    extension = filename.split('.')[-1]
    return f'{instance.title}/file/audio.{extension}'

'''------------------------------------------------------------------'''

def post_image_save(instance, filename):
    arr = [choice(string.ascii_letters) for _ in range(8)]
    pid = ''.join(arr)
    extension = filename.split('.')[-1]
    return f'{instance.post.title}/image/{pid}.{extension}'

def post_file_save(instance, filename):
    return f'{instance.post.title}/file/{filename}'

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
    date = models.DateField(_('일시'), blank=True, null=True, help_text='설교, 찬양, 기도에만 작성하세요.')
    title = models.CharField(_('제목'), max_length=50, blank=True)
    preacher = models.CharField(_('설교자'), max_length=20, blank=True, help_text='설교에만 작성하세요.')
    writer = models.ForeignKey(account, on_delete=models.SET(set_defautwriter_when_deleted), related_name='post')
    video = models.CharField(_('동영상'), max_length=255, blank=True, help_text='유튜브 주소를 입력하세요.')
    words = models.CharField(_('오늘의 말씀'), max_length=50, blank=True, help_text='설교에만 작성하세요.')
    content = RichTextUploadingField(verbose_name='내용', blank=True, null=True)
    views = models.IntegerField(_('조회수'), default=0)
    published = models.BooleanField(_('공개여부'), default=True)
    notice = models.BooleanField(_('공지사항'), default=False)
    image = models.TextField(_('사진'), blank=True)

    def __str__(self):
        return f'{self.get_div_display()} / {self.title}'

    def get_absolute_url(self):
        return f'/board/{self.div}/detail/{self.id}'

    @property
    def viewsup(self):
        self.views += 1
        self.save()

class PostFile(models.Model):

    class Meta:
        verbose_name = ('첨부파일')
        verbose_name_plural = ('첨부파일')

    post = models.ForeignKey(Post, on_delete=models.CASCADE, default='', verbose_name='게시글', related_name='file')
    file = models.FileField(_('첨부파일'), upload_to=post_file_save, blank=True)

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

# 쿼리삭제시 이미지, 비디오, 파일 삭제 #
@receiver(post_delete, sender=PostFile)
def submission_delete(sender, instance, **kwargs):
    instance.file.delete(False)