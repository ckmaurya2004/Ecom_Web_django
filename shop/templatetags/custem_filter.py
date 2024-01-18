from django import template

register = template.Library()

@register.filter(name="rate_set")
def rate_set(number):
    return f" { '$' }   {number} "


