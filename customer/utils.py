#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

from django.core import validators
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
# from customer.models import User

# 判断是否与邮箱或用户名相匹配
def get_right_user(accountname, pwd):
        user = authenticate(email=accountname, password=pwd)

        if user is None:
            return authenticate(username=accountname, password=pwd)
        return user

class CommonPasswordValidator(validators.BaseValidator):
    # See http://www.smartplanet.com/blog/business-brains/top-20-most-common-passwords-of-all-time-revealed-8216123456-8216princess-8216qwerty/4519  # noqa
    forbidden_passwords = [
        'password',
        '1234',
        '12345'
        '123456',
        '123456y',
        '123456789',
        'iloveyou',
        'princess',
        'monkey',
        'rockyou',
        'babygirl',
        'monkey',
        'qwerty',
        '654321',
        'dragon',
        'pussy',
        'baseball',
        'football',
        'letmein',
        'monkey',
        '696969',
        'abc123',
        'qwe123',
        'qweasd',
        'mustang',
        'michael',
        'shadow',
        'master',
        'jennifer',
        '111111',
        '2000',
        'jordan',
        'superman'
        'harley'
    ]
    message = _("Please choose a less common password")
    code = 'password'

    def __init__(self, password_file=None):
        self.limit_value = password_file

    def clean(self, value):
        return value.strip()

    def compare(self, value, limit):
        return value in self.forbidden_passwords

    def get_forbidden_passwords(self):
        if self.limit_value is None:
            return self.forbidden_passwords

password_validators = [
    validators.MinLengthValidator(6),
    CommonPasswordValidator
]


def normalise_email(email):
    """
    常规化email 大写变小写等
    :param email:
    :return:
    """
    print type(email)
    clean_email = email.strip()
    if '@' in clean_email:
        local, host = clean_email.split('@')
        return local + '@' +host.lower()
    return clean_email

# def authenticate_email(email=None, password=None):
#     try:
#         user = User.objects.get(email=email, password=password)
#     except:
#         user = None
#     print user

    # return user
