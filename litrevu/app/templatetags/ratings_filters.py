from django import template

register = template.Library()


@register.filter(name='stars')
def stars(value):
    return '★' * value + '☆' * (5 - value)
