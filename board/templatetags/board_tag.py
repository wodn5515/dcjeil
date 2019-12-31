from django import template
import re, os, datetime

register = template.Library()

@register.simple_tag
def td_no(value, total, start):
    return total-start-value

@register.filter
def url_target_blank(text):
    return text.replace('<a ', '<a target="_blank" ')
url_target_blank = register.filter(url_target_blank, is_safe = True)