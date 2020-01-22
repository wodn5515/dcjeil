from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_delete
from django.dispatch import receiver
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
from imagekit.utils import get_cache
from random import choice
from ckeditor.fields import RichTextField
from account.choice import OFFICE_CHOICES
from .choice import DIV_CHOICES, COMMUNITY
import string

# Create your models here.

# 슬라이드쇼 이미지 저장 #
def carousel_image_save(instance, filename):
    return f'data/home_carousel/{filename}'

# 섬기는사람들 이미지 저장 #
def server_image_save(instance, filename):
    return f'data/server/{instance.name}'

# 담임목사소개 이미지 저장 #  
def pastol_image_save(instance, filename):
    return f'data/pastolintro/담임목사소개'

# 커뮤니티 이미지 저장 # 
def community_image_save(instance, filename):
    return f'data/community/{instance.get_div_display()}'

# 홈화면 왼쪽 슬라이드쇼 #
class Carousel(models.Model):
    
    class Meta:
        verbose_name = ('홈페이지 슬라이드')
        verbose_name_plural = ('홈페이지 슬라이드')

    title = models.CharField(_('한줄설명'), max_length=15)
    image = models.ImageField(_('사진'), upload_to=carousel_image_save)
    order = models.IntegerField(_('순서'), help_text='낮을수록 먼저나옵니다.', default=0)

    def __str__(self):
        return f'{self.title}'

# 교회연혁 #
class History(models.Model):

    class Meta:
        verbose_name = ('교회연혁 관리')
        verbose_name_plural = ('교회연혁 관리')

    date = models.DateField(_('일시'))
    content = models.TextField(_('내용'))

    def __str__(self):
        return f'{self.content}'

# 섬기는 사람들 #
class Server(models.Model):

    class Meta:
        verbose_name = ('섬기는 사람들 관리')
        verbose_name_plural = ('섬기는 사람들 관리')

    name = models.CharField(_('이름'), max_length=5, blank=True)
    div = models.CharField(_('구분'), max_length=10, choices=DIV_CHOICES, blank=True)
    office = models.CharField(_('직분'), max_length=10, choices=OFFICE_CHOICES, blank=True)
    image = models.ImageField(_('사진'), upload_to=server_image_save, blank=True)
    tp = models.CharField(_('핸드폰'), max_length=15, blank=True, help_text = "'-' 를 제외한 숫자만 입력해주세요.")
    htp = models.CharField(_('집전화'), max_length=15, blank=True, help_text = "'-' 를 제외한 숫자만 입력해주세요.")
    email = models.EmailField(_('이메일'), blank=True)
    charge = models.CharField(_('담당사역'), max_length=50, blank=True)

    def __str__(self):
        return f'{self.get_div_display()} - {self.name} {self.get_office_display()}님'

class Pastol(models.Model):

    class Meta:
        verbose_name = ('담임목사소개 관리')
        verbose_name_plural = ('담임목사소개 관리')

    education = models.TextField(_('학력'))
    career = models.TextField(_('사역경력'))
    experience = models.TextField(_('활동경력'))
    image = models.ImageField(_('사진'), upload_to=pastol_image_save, blank=True)

    def __str__(self):
        return f'담임목사소개'

class Worship(models.Model):

    class Meta:
        verbose_name = ('예배안내 관리')
        verbose_name_plural = ('예배안내 관리')
    
    content = RichTextField(blank=True)

    def __str__(self):
        return f'예배안내 시간표'

class Community(models.Model):
    
    class Meta:
        verbose_name = ('커뮤니티 관리')
        verbose_name_plural = ('커뮤니티 관리')

    div = models.CharField(_('구분'), max_length=10, choices=COMMUNITY, blank=True)
    image = models.ImageField(_('사진'), blank=True)
    title = models.TextField(_('표어'), blank=True)
    goal = models.TextField(_('교육목표'), blank=True)
    worship = models.TextField(_('예배안내'), blank=True)
    server = models.TextField(_('섬기는 사람들'), blank=True)

    def __str__(self):
        return f'{self.get_div_display()}'


# 데이터 삭제시 사진삭제 #
@receiver(post_delete, sender=Carousel)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

@receiver(post_delete, sender=Server)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

@receiver(post_delete, sender=Pastol)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)

@receiver(post_delete, sender=Community)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)