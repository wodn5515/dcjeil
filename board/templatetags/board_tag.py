from django import template
import re, os

register = template.Library()

@register.simple_tag
def td_no(value, total, start):
    return total-start-value