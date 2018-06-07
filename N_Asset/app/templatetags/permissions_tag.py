from django import template
register = template.Library()

@register.simple_tag
def any_function():
    return 'Rimba'