from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from .models import PostImage

import os

@receiver(post_delete, sender=PostImage)
def postimage_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)

@receiver(pre_save, sender=PostImage)
def postimage_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_image = PostImage.objects.get(pk=instance.pk).image
    except:
        return False

    new_image = instance.image
    if new_image != old_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)