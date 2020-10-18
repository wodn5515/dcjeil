from django import template
from django.utils import timezone
from menu.models import Submenu, Mainmenu
import re, os, datetime

register = template.Library()

@register.simple_tag
def td_no(value, start):
    return value+start

@register.filter
def url_target_blank(text):
    return text.replace('<a ', '<a target="_blank" ')
url_target_blank = register.filter(url_target_blank, is_safe = True)

@register.filter
def youtube_embed(link):
    if link.find('.com') == -1:
            link = link.split('/')[-1]
    else:
        start = link.find('v=') + 2
        link = link[start:start+11]
    return "http://www.youtube.com/embed/" + link

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

@register.filter
def is_mobile(user_agent):
    return True if 'Mobi' in user_agent else False