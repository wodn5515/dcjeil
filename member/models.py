from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin, Permission, GroupManager
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from menu.models import Submenu
from data.models import Duty, Belong
from .choice import *

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, uid, name, password, email):
        user = self.model(
            uid=uid,
            name=name,
            email=email
            )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, uid, name, password, email):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여한다. 
        """
        user = self.create_user(
            uid=uid,
            name=name,
            password=password,
            email=email
        )

        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    

class AdminPermissionGroup(models.Model):
    name = models.CharField(_('그룹명'), max_length=80, unique=True)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('권한'),
        blank=True,
    )

    objects = GroupManager()

    class Meta:
        verbose_name = _('관리자페이지 권한')
        verbose_name_plural = _('관리자페이지 권한')

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)
    
    
class BoardPermissionGroup(models.Model):
    name = models.CharField(_('그룹명'), max_length=80, unique=True)
    permissions = models.ManyToManyField(
        Submenu,
        verbose_name=_('게시판'),
        blank=True,
        limit_choices_to={'m_type__contains':'list'}
    )

    class Meta:
        verbose_name = _('게시판 권한')
        verbose_name_plural = _('게시판 권한')
        
    def __str__(self):
        return self.name
    
        
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(_('이름'), max_length=5, default='')
    is_media = models.BooleanField(_("미디어팀"), default=False)
    is_active = models.BooleanField(_('승인'), default=False)
    is_staff = models.BooleanField(_('스태프'), default=False, help_text=_('◈ 관리자페이지 접속권한'))
    is_superuser = models.BooleanField(_('관리자'), default=False, help_text=_('◈ 최고등급의 관리자권한'))
    is_social = models.BooleanField(_('소셜로그인'), default=False)
    is_registered = models.BooleanField(_('교인여부'), default=False, help_text=_('◈ 본 교회 교인이시면 체크해주세요.'))
    date_joined = models.DateTimeField(_('가입날짜'), default=timezone.now)
    uid = models.CharField(
        _('ID'),
        max_length = 50,
        unique = True,
        error_messages = {
            'unique' : _("이미 가입된 아이디입니다."),
        },
    )
    email = models.EmailField(
        _('이메일'),
        help_text=_('◈ 회원정보를 찾을 때 필요합니다'),
        unique=True,
        error_messages = {
            'unique' : _("이미 가입된 이메일입니다."),
        }
    )
    tp = models.CharField(
        _('연락처'),
        max_length=15,
        help_text=_("◈ ' - '를 제외하고 입력해주세요."),
        unique=True,
        null=True,
        error_messages = {
            'unique' : _("이미 가입된 연락처입니다."),
        }
    )
    duty = models.ForeignKey(
        Duty,
        verbose_name=_('직분'),
        on_delete=models.SET_NULL,
        null=True
    )
    belong = models.ForeignKey(
        Belong,
        verbose_name=_('소속'),
        on_delete=models.SET_NULL,
        null=True
    )
    adminpermissiongroups = models.ManyToManyField(
        AdminPermissionGroup,
        verbose_name=_('관리자페이지 권한'),
        blank=True
    )
    boardpermissiongroups = models.ManyToManyField(
        BoardPermissionGroup,
        verbose_name=_('게시판 권한'),
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = ['name', 'email']

    class Meta:
        verbose_name = _('회원')
        verbose_name_plural = _('회원')
        ordering = ('-date_joined',)

    def __str__(self):
        return f'{self.name}'