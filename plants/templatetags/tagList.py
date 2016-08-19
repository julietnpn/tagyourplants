from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
def tagSet(value):
    tagList = set()
    if value:
        tagList = eval(value)
    return tagList
