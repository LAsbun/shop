#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

from django.conf.urls import url, patterns


from customer.views import index, registration, login, logout
urlpatterns = [
    url(r"^login/$", login, name='login'),
    url(r'^regisration/$', registration, name='registration'),
    # url(r'^forgetpassword/$', forgetpassword, name='forgetpassword'),
    url(r'^logout', logout, name='logout')
]