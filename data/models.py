from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_delete
from django.dispatch import receiver
from imagekit.models import ImageSpecField
from imagekit.processors import Thumbnail
from imagekit.utils import get_cache
from random import choice
import string

# Create your models here.

# 교회연혁 #
class History(models.Model):

    class Meta:
        verbose_name = ('교회연혁')
        verbose_name_plural = ('교회연혁 관리')

    date = models.DateField(_('일시'))
    content = models.TextField(_('내용'))

    def __str__(self):
        return f'{{content}}'