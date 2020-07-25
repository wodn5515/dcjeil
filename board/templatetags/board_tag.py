from django import template
from django.utils import timezone
from data.models import Submenu, Mainmenu
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

@register.filter
def get_parameters(url):
    return '?' + url.split('?')[1] if '?' in url else ''

@register.filter_function
def order_by(queryset, args):
    args = [x.strip() for x in args.split(',')]
    return queryset.order_by(*args)

@register.filter
def get_main_title(idx):
    return Mainmenu.objects.get(order=int(idx)).name

@register.filter
def subquery(no):
    sub_menu = Submenu.objects.filter(mainmenu=no).order_by('order')
    return sub_menu