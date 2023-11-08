from django import template

register = template.Library()

@register.filter(name='split_integer_and_decimal')
def split_integer_and_decimal(value):
    
    try:
        price = str(value).split('.')
        return price

    except (ValueError, ZeroDivisionError):
        return None
    

