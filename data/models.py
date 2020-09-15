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
from .choice import COMMUNITY, MENUTYPE
import string

# Create your models here.

# 슬라이드쇼 이미지 저장 #
def carousel_image_save(instance, filename):
    return f'data/home_carousel/{filename}'

# 팝업 이미지 저장 #
def popup_image_save(instance, filename):
    return f'data/popup/{filename}'

# 섬기는사람들 이미지 저장 #
def server_image_save(instance, filename):
    return f'data/server/{instance.name}'

# 담임목사소개 이미지 저장 #  
def pastol_image_save(instance, filename):
    return f'data/pastolintro/담임목사소개'

# 커뮤니티 이미지 저장 # 
def community_image_save(instance, filename):
    return f'data/community/{instance.get_div_display()}'

###############################################################

# 메뉴 관리 #
class Mainmenu(models.Model):

    class Meta:
        verbose_name = ('메인메뉴 관리')
        verbose_name_plural = ('메인메뉴 관리')

    name = models.CharField(_('메뉴명'), max_length=100)
    order = models.IntegerField(_('순서'), unique=True, help_text="낮을수록 먼저 배치됩니다")

    def __str__(self):
        return f'{self.name}'

class Submenu(models.Model):

    class Meta:
        verbose_name = ('서브메뉴 관리')
        verbose_name_plural = ('서브메뉴 관리')
    
    mainmenu = models.ForeignKey(Mainmenu, on_delete=models.CASCADE, verbose_name='메인메뉴', related_name='submenu')
    name = models.CharField(_('메뉴명'), max_length=100)
    order = models.IntegerField(_('순서'), help_text="낮을수록 먼저 배치됩니다")
    m_type = models.CharField(_('타입'), choices=MENUTYPE, max_length=50, default='list')
    is_allowed_to_not_superuser = models.BooleanField(_('일반회원 작성가능여부'), default=False)

    def __str__(self):
        return f'{self.mainmenu.name} - {self.name}'

    def get_absolute_url(self):
        return f'/board/{self.mainmenu.order}0{self.order}' if len(str(self.order)) == 1 else f'/board/{self.mainmenu.order}{self.order}'

    def get_full_menu(self):
        return f'{self.mainmenu.order}0{self.order}' if len(str(self.order)) == 1 else f'{self.mainmenu.order}{self.order}'

# 인사말 #
class Welcome(models.Model):

    class Meta:
        verbose_name = ('인사말 관리')
        verbose_name_plural = ('인사말 관리')

    content = RichTextUploadingField(default='')

    def __str__(self):
        return f'인사말'

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

# 우리의 비전 #
class Vision(models.Model):

    class Meta:
        verbose_name = ('우리의 비전 관리')
        verbose_name_plural = ('우리의 비전 관리')

    content = RichTextUploadingField(default='')

    def __str__(self):
        return f'우리의 비전'


# 찾아오시는 길 #
class Wayto(models.Model):

    class Meta:
        verbose_name = ('찾아오시는 길 관리')
        verbose_name_plural = ('찾아오시는 길 관리')

    content = RichTextUploadingField(default='')

    def __str__(self):
        return f'찾아오시는 길'


# 양육시스템 #
class Nurture(models.Model):

    class Meta:
        verbose_name = ('양육시스템 관리')
        verbose_name_plural = ('양육시스템 관리')

    content = RichTextUploadingField(default='')

    def __str__(self):
        return f'양육시스템'

# 섬기는 사람들 #
class Server(models.Model):

    class Meta:
        verbose_name = ('섬기는 사람들 관리')
        verbose_name_plural = ('섬기는 사람들 관리')

    content = RichTextUploadingField(default='')

    def __str__(self):
        return f'섬기는 사람들'

class Pastol(models.Model):

    class Meta:
        verbose_name = ('담임목사소개 관리')
        verbose_name_plural = ('담임목사소개 관리')

    content = RichTextUploadingField(default='')

    def __str__(self):
        return f'담임목사소개'

class Worship(models.Model):

    class Meta:
        verbose_name = ('예배안내 관리')
        verbose_name_plural = ('예배안내 관리')
    
    content = RichTextUploadingField(default='')

    def __str__(self):
        return f'예배안내'

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
    youtube = models.CharField(_('유튜브링크'), max_length=255,  blank=True, default='')

    def __str__(self):
        return f'{self.get_div_display()}'

    def get_youtube_url(self):
        return 'https://www.youtube.com/channel/{}'.format(self.youtube)


# 데이터 삭제시 사진삭제 #
@receiver(post_delete, sender=Carousel)
def submission_delete_carousel(sender, instance, **kwargs):
    instance.image.delete(False)

@receiver(post_delete, sender=Server)
def submission_delete_server(sender, instance, **kwargs):
    instance.image.delete(False)

@receiver(post_delete, sender=Pastol)
def submission_delete_pastol(sender, instance, **kwargs):
    instance.image.delete(False)

@receiver(post_delete, sender=Community)
def submission_delete_community(sender, instance, **kwargs):
    instance.image.delete(False)