from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from .choice import *

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, uid, name, password):
        user = self.model(
            uid=uid,
            name=name,
            )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, uid, name, password):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여한다. 
        """
        user = self.create_user(
            uid=uid,
            name=name,
            password=password,
        )

        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user
    
class PermissionsGroup(models.Model):
    name = models.CharField(_('그룹명'), max_length=100, default='')
    
    class Meta:
        verbose_name = "그룹관리"
        verbose_name_plural = "그룹관리"
        
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(_('이름'), max_length=5, default='')
    is_active = models.BooleanField(_('승인'), default=False)
    is_staff = models.BooleanField(_('스태프'), default=False, help_text="관리자페이지 접속권한")
    is_superuser = models.BooleanField(_('관리자'), default=False, help_text="최고등급의 관리자권한")
    is_social = models.BooleanField(_('소셜로그인'), default=False)
    date_joined = models.DateTimeField(_('가입날짜'), default=timezone.now)
    uid = models.CharField(_('ID'), max_length = 50, unique = True,
        error_messages = {
            'unique' : _("이미 가입된 아이디 입니다."),
        },
    )

    objects = UserManager()

    USERNAME_FIELD = 'uid'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = _('회원')
        verbose_name_plural = _('회원')
        ordering = ('-date_joined',)

    def __str__(self):
        return f'{self.name}'
