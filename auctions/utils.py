
import re
import requests
from dotenv import load_dotenv
import os
# from .models import AuctionListing

load_dotenv()
UPSPLASH_API_KEY = os.getenv('UNSPLASH_API_KEY')


def print_normal_message(obj_text):
    print('################')
    print(obj_text)
    print('################')
    

def print_error_message(obj_text):
    print('!!!!!!!!!!!!!!!!')
    print(obj_text)
    
    
    
def integrity_check(func):
    from django.db import IntegrityError
    
    def wrapper(instance, *args, **kwargs):
        message = kwargs.pop('failed_message', "An Integrity Error occurred")
        try:
            func(instance, *args, **kwargs)
            return {'status': 'success'}
        except IntegrityError:

            return {'status': 'failed', 'failed_message': message}

    return wrapper


def create_default_category(sender, **kargs):
    from .models import Category
    
    try:
        Category.objects.get_or_create(name='other')
    except InterruptedError:
        pass

# For checking category creation input
# Only accept english characters and contains no spaces
def only_contains_word_or_empty_string(string):
    pattern = re.compile(r"[a-z]*", flags=re.IGNORECASE)
    match = pattern.fullmatch(string=string)
    return True if match else False


def get_unsplash_img_url(query):
    url = 'https://api.unsplash.com/search/photos'
    params = {
        'query': query,
        'client_id': UPSPLASH_API_KEY,
        'per_page': 1
    }
    res = requests.get(url, params=params)
    if res.status_code == 200:
        data = res.json()
        first_image_url = data['results'][0]['urls']['regular']
        return first_image_url
    else:
        return None

# def get_highest_none_null_bid_price(listing_id):
#     listing = AuctionListing.objects.get(id=listing)
#     return listing.bids.all().order_by('-price').first()
