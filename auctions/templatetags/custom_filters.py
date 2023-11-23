from django import template

register = template.Library()

@register.filter(name='split_integer_and_decimal')
def split_integer_and_decimal(value):
    
    try:
        price = str(value).split('.')
        return price

    except (ValueError, ZeroDivisionError):
        return None
    
@register.simple_tag
def get_highest_user_bid(listing, user):
    
    return listing.bids.filter(user=user).order_by('-price').first() # highest user bid
