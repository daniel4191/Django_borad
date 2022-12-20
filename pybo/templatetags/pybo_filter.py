from django import template

# code line
register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg
