#!/usr/bin/env python
# coding:utf-8

import random
from math import ceil

from django.shortcuts import render_to_response, redirect
from django.http import HttpResponseNotFound
from django.template.context import RequestContext

from category.models import Product, Category
from shop.utils import get_list_randon_int, Paginor, PagiInfo, try_int
from basket.models import Basket
# Create your views here.


product_total = Product.objects.count()
each_page_num = 12
max_page_nums = product_total/each_page_num
if product_total % each_page_num != 0:
    max_page_nums += 1


def index(request):
    msg = {}

    # ---------------
    # Login
    username = request.session.get('is_login', None)
    if username:
        msg['user'] = username
        msg['logout'] = 'Logout'

    # basket
    try:
        bsobj = Basket.objects.get(owner__username=username)
    except:
        bsobj = None
    msg['basket'] = bsobj

    #-----------------

    # paginator
    product_list = Product.objects.all()[:each_page_num]

    pageobj = PagiInfo(1, product_total, each_page_num)
    page = Paginor(1, pageobj.total_pages,url_string='/category/product_list/', )
    msg['paginator'] = page
    #product
    msg['product_list'] = product_list


    #category
    try:
        cate_list = Category.objects.filter(numchild__gt=0)
        # print dir(cate_list[0])
        # print cate_list
    except :
        cate_list = Category.objects.all()
        # print "ss"
    msg['cate_list'] = cate_list

    # basket
    next_url = request.GET.get('next', None)
    # print next_url
    msg['next_url'] = next_url



    return render_to_response('index.html', msg, context_instance=RequestContext(request))


def product_detail(request, id):
    msg = {}
    try:
        product = Product.objects.get(id=id)
        # print product.attribute_values.all()[2]
    except Exception, e:
        # print e
        return redirect(index)

    total_product = Product.objects.count()
    # print total_product,'------'

    related_product = map(get_relate_product, get_list_randon_int(6, stop=total_product))

    msg['attr_list'] = product.attribute_values.all()

    # print msg['attr_list'][2].value_as_text
    # msg['image'] = msg['attr_list'][0]
    msg['product'] = product
    msg['related_product'] = related_product
    msg['side_product'] = map(get_relate_product, get_list_randon_int(2, stop=total_product))

     # ---------------
    # Login
    username = request.session.get('is_login', None)
    if username:
        msg['user'] = username
        msg['logout'] = 'Logout'

    # basket
    try:
        bsobj = Basket.objects.get(owner__username=username)
    except:
        bsobj = None
    msg['basket'] = bsobj
    # -----------------
    return  render_to_response('product_detail.html', msg, context_instance=RequestContext(request))

def get_relate_product(id):
    # 得到相关的商品
    try:
        return Product.objects.get(id=id)
    except:
        return

def product_list(request, page):


    msg = {}
    # product
    page_num = try_int(page)

    if page_num > max_page_nums:
        # return redirect(product_list)
        return render_to_response('error.html')

    pageobj = PagiInfo(page_num, product_total, each_page_num)

    page = Paginor(page_num, pageobj.total_pages, '/category/product_list/')

    product_list = Product.objects.all()[pageobj.start:pageobj.end]
    msg['paginator'] = page
    msg['product_list'] = product_list
    # ---------------
    # Login
    username = request.session.get('is_login', None)
    if username:
        msg['user'] = username
        msg['logout'] = 'Logout'

    # basket
    try:
        bsobj = Basket.objects.get(owner__username=username)
    except:
        bsobj = None
    msg['basket'] = bsobj
    # -----------------
    return render_to_response('index.html', msg)


def category_list(request, cate):
    print cate
    msg = {}
    try:
        page = try_int(request.GET.get('page', 1))

        cate_obj = Category.objects.get(id=cate)
        product_list = Product.objects.filter(category=cate_obj)

        # paginator
        pageobj = PagiInfo(1, len(product_list), each_page_num)
        page = Paginor(page, pageobj.total_pages, '?page=')
        msg['paginator'] = page

        msg['product_list'] = product_list[pageobj.start:pageobj.end]

        #category
        try:
            cate_list = Category.objects.filter(numchild__gt=0)
            # print dir(cate_list[0])
            # print cate_list
        except Exception, e:
            print e
            cate_list = Category.objects.all()
            # print "ss"

        msg['cate_list'] = cate_list

        msg['cate_id'] = cate
         # ---------------
        # Login
        username = request.session.get('is_login', None)
        if username:
            msg['user'] = username
            msg['logout'] = 'Logout'

        # basket
        try:
            bsobj = Basket.objects.get(owner__username=username)
        except:
            bsobj = None
        msg['basket'] = bsobj
        # -----------------
        return render_to_response('categoties.html', msg)

    except Exception, e:
        print e
        return render_to_response('error.html')