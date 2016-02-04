#!/usr/bin/env python
from django.utils.crypto import get_random_string

# Based on Django's SECRET_KEY hash generator
# https://github.com/django/django/blob/9893fa12b735f3f47b35d4063d86dddf3145cb25/django/core/management/commands/startproject.py

def gen_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = get_random_string(50, chars)
    with open(".secret.txt", "w") as f:
        f.write(secret_key)
    return secret_key

def get_key():
    try:
        with open(".secret.txt") as f:
            return f.read().strip()
    except IOError:
        return gen_key()
if __name__ == '__main__':
    print(get_key())
