from django import template
from django.utils import timezone
import re, os, datetime

register = template.Library()

@register.simple_tag
def td_no(value, total, start):
    return total-start-value

@register.filter
def url_target_blank(text):
    return text.replace('<a ', '<a target="_blank" ')
url_target_blank = register.filter(url_target_blank, is_safe = True)

@register.filter
def filename(value):
    return value.split('/')[-1]

@register.filter
def post_new(date):
    day_difference = (timezone.now()-date).days
    return True if day_difference < 7 else False

@register.filter
def submenu_idx(idx):
    idx = str(idx)
    return '0' + idx if len(idx) == 1 else idx
