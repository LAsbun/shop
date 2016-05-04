#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

import random
import string

from django import forms
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.utils.http import is_safe_url
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy

from customer.utils import password_validators, get_right_user
# from customer.models import User

from django.contrib.auth.models import User

def generate_username():
    # Python 3 uses ascii_letters. If not available, fallback to letters
    try:
        letters = string.ascii_letters
    except AttributeError:
        letters = string.letters
    uname = ''.join([random.choice(letters + string.digits + '_')
                     for i in range(30)])
    try:
        User.objects.get(username=uname)
        return generate_username()
    except User.DoesNotExist:
        return uname


class UserLoginForm(forms.Form):
    accountname = forms.CharField(label='用户名/邮箱', min_length=1,

    )
    password = forms.CharField(
        label = _('Password'), widget=forms.PasswordInput,
        validators = password_validators
    )

    def clean_accountname(self):
        accountname = self.cleaned_data.get('accountname', '')

        if not (User.objects.filter(email__iexact=accountname).exists()
                    or User.objects.filter(username__iexact=accountname).exists()):
            raise  forms.ValidationError(
                '用户名或邮箱不存在'
            )
        return accountname

    def clean_password(self):
        accountname = self.cleaned_data.get('accountname', '')
        pwd = self.cleaned_data.get('password', '')
        user = get_right_user(accountname=accountname, pwd=pwd)
        if user is None:
            raise forms.ValidationError(
                '账号或密码错误'
            )
        return pwd




class EmailUserCreationForm(forms.ModelForm):
    username = forms.CharField(label=_('username'))
    email = forms.EmailField(label='邮箱')
    password1 = forms.CharField(
        label = _('Password'), widget=forms.PasswordInput,
        validators = password_validators
    )
    password2 = forms.CharField(
        label='确认密码', widget=forms.PasswordInput
    )


    class Meta:
        model=User
        fields = ('email', 'username',)

    def clean_email(self):
        email = self.cleaned_data['email']

        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "邮箱已存在"
            )
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1', '')
        password2 = self.cleaned_data.get('password2', '')
        if password1 != password2:
            raise  forms.ValidationError(
                # _('The password mismatch the former one.')
                '密码不一致'
            )
