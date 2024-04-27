# myapp/templatetags/my_tags.py
from django import template
from ..utils import calculate_order_cash

register = template.Library()

@register.simple_tag
def call_calculate_order_cash(cash, payed=False):
    return calculate_order_cash(cash, payed)
