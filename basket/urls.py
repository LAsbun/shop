#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

from django.conf.urls import url, static

from .views import add_to_basket

urlpatterns = [

    url(r'^add_to_basket/(?P<pk>\d+)/$', add_to_basket, name='add_to_basket')

]


