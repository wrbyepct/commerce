
import re


def only_contains_word_or_empty_string(string):
    pattern = re.compile(r"[a-z]*", flags=re.IGNORECASE)
    match = pattern.fullmatch(string=string)
    return True if match else False
        

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
        message = kwargs.pop('message', "An Integrity Error occurred")
        try:
            func(instance, *args, **kwargs)
            return {'status': 'success'}
        except IntegrityError:

            return {'status': 'failed', 'message': message}

    return wrapper


def create_default_category(sender, **kargs):
    from .models import Category
    
    try:
        Category.objects.get_or_create(name='other')
    except InterruptedError:
        pass
    
