#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

from django.conf.urls import url, static
from django.conf import settings

from category.views import product_detail, product_list, category_list


urlpatterns = [
   # url(r'^product_add$', )
    url(r'^product/(?P<id>\d+)/?$', product_detail, name='product_detail', ),
    url(r'^product_list/(?P<page>\d*)/?$', product_list, name="product_list"),
    url(r'^category_list/(?P<cate>\d+)/?$', category_list, name='category_list'),
]