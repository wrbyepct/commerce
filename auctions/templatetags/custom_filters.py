from django import template

register = template.Library()

@register.filter(name='convert_price')
def divide(value):
    price = str(value).split('.')
    
    try:
        return price

    except (ValueError, ZeroDivisionError):
        return None