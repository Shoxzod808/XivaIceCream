""" # myapp/templatetags/my_tags.py
from django import template
from ..utils import get_text, get_document

register = template.Library()

@register.simple_tag
def call_get_text(title, lang, button=False):
    return get_text(title, lang, button)

@register.filter
def call_get_document(data):
    return get_document(data.id) """