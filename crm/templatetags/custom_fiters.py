from django import template

register = template.Library()

@register.filter
def multiply(value1, value2):
    try:
        return value1 * value2
    except (TypeError, ValueError):
        return 0