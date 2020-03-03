from django import template
import util

register = template.Library()


@register.simple_tag(takes_context=True)
def subtract(context, int1=0, int2=0):
    return int1 - int2


@register.simple_tag(takes_context=True)
def format_number(context, num, code=""):
    if code == "":
        return util.format_number(num)
    else:
        return util.format_number(num, code)
