import datetime
import random
import string
import os
from django.utils import timezone

from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_key_generator(instance):
    a = random.randint(2222, 5555)
    b = random.randint(5556, 7777)
    c = random.randint(7778, 9999)
    choices = (a, b, c)
    key = random.choice(choices)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(token_no=key).exists()
    if qs_exists:
        return random.randint(2222, 9999)
    return key


# def unique_key_generator(instance):
#     """
#     This is for a Django project with an key field
#     """
#     size = random.randint(1, 8)
#     key = random_string_generator(size=size)
#
#     Klass = instance.__class__
#     qs_exists = Klass.objects.filter(token_no=key).exists()
#     if qs_exists:
#         return random_string_generator(instance)
#     return key


def unique_token_no_generator(instance):
    """
    This is for a Django project with an token_no field
    """
    token_new_no = unique_key_generator(instance)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(token_no=token_new_no).exists()
    if qs_exists:
        return unique_key_generator(instance)
    return token_new_no
