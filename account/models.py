from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, username, name, tp, birthday, email, office, password):
        user = self.model(
            username=username,
            name=name,
            tp=tp,
            birthday=birthday,
            email=email,
            office=office
            )
        
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, tp, birthday, email, office, password):
        """
        주어진 이메일, 닉네임, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여한다. 
        """
        user = self.create_user(
            username=username,
            name=name,
            password=password,
            tp=tp,
            birthday=birthday,
            email=email,
            office=office
        )

        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(_('이름'), max_length = 5)
    birthday = models.CharField(_('생년월일'), max_length = 8)
    office = models.CharField(_('직분'),max_length = 10)
    parish = models.CharField(_('교구'), max_length = 10, blank = True)
    address = models.CharField(_('주소'), max_length = 255, blank = True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('가입날짜'), default=timezone.now)
    username = models.CharField(_('ID'), max_length = 15, unique = True,
        error_messages = {
            'unique' : _("이미 가입된 아이디 입니다."),
        },
    )
    tp = models.CharField(_('연락처'), max_length = 15, unique = True,
        error_messages = {
            'unique' : _("이미 가입된 연락처 입니다.")
        }
    )
    email = models.EmailField(_('이메일'), max_length = 255, unique = True,
        error_messages = {
            'unique' : _("이미 가입된 이메일 입니다."),
        },
    )

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'tp', 'email', 'birthday', 'office']

    class Meta:
        verbose_name = _('회원')
        verbose_name_plural = _('회원')
        ordering = ('-date_joined',)

    def __str__(self):
        if self.parish:
            return f'{self.parish} - {self.name}'
        else:
            return f'{self.name}'