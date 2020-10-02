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
from member.choice import OFFICE_CHOICES
from .choice import COMMUNITY
import string

# Create your models here.

# 슬라이드쇼 이미지 저장 #
def carousel_image_save(instance, filename):
    return f'data/home_carousel/{filename}'

# 팝업 이미지 저장 #
def popup_image_save(instance, filename):
    return f'data/popup/{filename}'

# 커뮤니티 이미지 저장 # 
def community_image_save(instance, filename):
    return f'data/community/{instance.get_div_display()}'

###############################################################


# 팝업 #
class Popup(models.Model):
    
    class Meta:
        verbose_name = ('팝업 관리')
        verbose_name_plural = ('팝업 관리')

    title = models.CharField(verbose_name='한줄설명', max_length=15)
    image = models.ImageField(_('사진'), upload_to=popup_image_save)
    
    def __str__(self):
        return '{}'.format(self.title)

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

class Community(models.Model):
    
    class Meta:
        verbose_name = ('교육부서 관리')
        verbose_name_plural = ('교육부서 관리')

    div = models.CharField(_('구분'), max_length=10, choices=COMMUNITY, blank=True)
    image = models.ImageField(_('사진'), blank=True, upload_to=community_image_save)
    title = models.TextField(_('표어'), blank=True)
    goal = RichTextUploadingField(verbose_name=('교육목표'), blank=True)
    worship = models.TextField(_('예배안내'), blank=True)
    server = RichTextUploadingField(verbose_name=('섬기는 사람들'), blank=True)
    youtube = models.CharField(_('유튜브링크'), max_length=255, blank=True, default='')

    def __str__(self):
        return f'{self.get_div_display()}'


# 데이터 삭제시 사진삭제 #
@receiver(post_delete, sender=Carousel)
def submission_delete_carousel(sender, instance, **kwargs):
    instance.image.delete(False)
    
@receiver(post_delete, sender=Community)
def submission_delete_community(sender, instance, **kwargs):
    instance.image.delete(False)
    
    
###############################################################################################
########################################## Abandoned ##########################################
###############################################################################################
                                                                                        #######
# 섬기는사람들 이미지 저장 #                                                              #######
def server_image_save(instance, filename):                                              #######
    return f'data/server/{instance.name}'                                               #######
                                                                                        #######
# 담임목사소개 이미지 저장 #                                                              #######
def pastol_image_save(instance, filename):                                              #######                                 
                                                                                        #######
    return f'data/pastolintro/담임목사소개'                                              #######
                                                                                        #######
###############################################################################################
########################################## Abandoned ##########################################
###############################################################################################