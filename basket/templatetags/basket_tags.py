#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

from django import template

from shop.utils import try_float

register = template.Library()

@register.filter(name='mul')
def multiply(value, token):
    return try_float(value)*try_float(token)

