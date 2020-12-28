from django.db import models
from django.utils.translation import ugettext_lazy as _
from .choices import PARISH

# Create your models here.


def new_year_eve_word_upload(instance, filename):
    ext = filename.split(".")[-1]
    return f"2021word/{instance.get_parish_display()}-{instance.name}.{ext}"


class NewYearEveWord(models.Model):
    name = models.CharField(_("이름"), max_length=5, default="")
    parish = models.CharField(_("교구"), max_length=10, choices=PARISH)
    words = models.ImageField(_("말씀"), upload_to=new_year_eve_word_upload)

    class Meta:
        verbose_name = _("송구영신예배 말씀뽑기")
        verbose_name_plural = _("송구영신예배 말씀뽑기")

    def __str__(self):
        return f"{self.get_parish_display()}-{self.name}"