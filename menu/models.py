from django.db import models
from django.utils.translation import ugettext_lazy as _
from ckeditor_uploader.fields import RichTextUploadingField
from .choices import MENUTYPE


# Create your models here.
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
    is_allowed_to_all = models.BooleanField(_('전체작성가능'), default=False)
    exposure_home = models.IntegerField(_('홈 화면 노출 여부'), default=0, help_text="<table><tbody><tr><td>1</td><td>2</td></tr><tr><td>3</td><td>4</td></tr></tbody></table>")

    def __str__(self):
        return f'{self.mainmenu.name} - {self.name}'

    def get_absolute_url(self):
        return f'/board/{self.mainmenu.order}0{self.order}' if len(str(self.order)) == 1 else f'/board/{self.mainmenu.order}{self.order}'

    def get_full_menu(self):
        return f'{self.mainmenu.order}0{self.order}' if len(str(self.order)) == 1 else f'{self.mainmenu.order}{self.order}'

class FixedMenu(models.Model):
    menu = models.ForeignKey(Submenu, limit_choices_to={'m_type':'fixed'}, on_delete=models.CASCADE)
    content = RichTextUploadingField(default="")
    
    class Meta:
        verbose_name = "고정형메뉴 관리"
        verbose_name_plural = "고정형메뉴 관리"
        
    def __str__(self):
        return f'{self.menu}'
