#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

from django.conf.urls import url, static
from django.conf import settings

from category.views import product_detail


urlpatterns = [
   # url(r'^product_add$', )
    url(r'^product/(?P<id>\d+)/', product_detail, name='product_detail', )
]