#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

from django.conf.urls import url, static

from .views import add_to_basket, show_basket, remove_product_line

urlpatterns = [

    url(r'^add_to_basket/(?P<pk>\d+)/?$', add_to_basket, name='add_to_basket'),
    url(r'^show_basket/?$', show_basket, name='show_basket'),
    url(r'^remove_product_line/?$', remove_product_line, name='remove_product_line'),

]


