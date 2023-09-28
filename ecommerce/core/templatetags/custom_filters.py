from django import template

register = template.Library()

@register.filter
def round_down(value):
    return int(value)
