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
from member.models import User as account
from .choices import Divs
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