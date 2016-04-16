#!/usr/bin/env python
# coding:utf-8

import random

from django.shortcuts import render_to_response, redirect

from category.models import Product
from category.utils import get_list_randon_int

# Create your views here.
def index(request):
    msg = {}
    username = request.session.get('is_login', None)
    if username:
        msg['user'] = username
        msg['logout'] = 'Logout'

    # product
    product_list = Product.objects.all()
    msg['product_list'] = product_list

    return render_to_response('index.html', msg)

def product_detail(request, id):
    msg = {}
    try:
        product = Product.objects.get(id=id)
        # print product.attribute_values.all()[2]
    except Exception, e:
        # print e
        return redirect(index)

    total_product = Product.objects.count()
    print total_product,'------'

    related_product = map(get_relate_product, get_list_randon_int(6, stop=total_product))

    msg['attr_list'] = product.attribute_values.all()
    # print msg['attr_list'][2].value_as_text
    msg['image'] = msg['attr_list'][0]
    msg['product'] = product
    # print len(related_product)
    msg['related_product'] = related_product
    return  render_to_response('category/product_detail.html', msg)

def get_relate_product(id):
    # 得到相关的商品
    try:
        return Product.objects.get(id=id)
    except:
        return