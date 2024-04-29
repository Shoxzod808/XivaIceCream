# myapp/templatetags/my_tags.py
from django import template
from ..utils import calculate_driver_cash

register = template.Library()

@register.simple_tag
def call_calculate_driver_cash(driver, payed=False):
    return calculate_driver_cash(driver, payed)
