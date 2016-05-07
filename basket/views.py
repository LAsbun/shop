#coding:utf-8
from datetime import datetime
import json

from django.shortcuts import render_to_response, HttpResponse
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.template import RequestContext
# Create your views here.

from category.views import index
from .models import Basket, Line
from category.models import Product
from shop.utils import try_int

@login_required(login_url='/customer/login')
def add_to_basket(request, pk):
    msg = {}

    if request.method == 'POST':
        user = request.session['is_login']
        quantity = try_int(request.POST.get('quantity', 1))
        print quantity, user
        try:
            if Basket.objects.get(owner__username=user):
                bsobj = Basket.objects.get(owner__username=user)
            else:
                bsobj = Basket.objects.create(owner=User.objects.get(username=user))
                bsobj.save()

            try:
                lineonj=Line.objects.get(product__id=pk)
            except:
                lineonj = None


            if lineonj:
                if lineonj.quantity + quantity >= lineonj.product.store_count:
                    lineonj.quantity = lineonj.product.store_count
                else:
                    lineonj.quantity = lineonj.quantity + quantity
            else:

                lineonj = Line.objects.create(
                    basket=bsobj, product=Product.objects.get(id=pk), quantity=quantity,
                    date_create=datetime.now()
                )
            lineonj.save()

        except Exception, e:
            print e
            return redirect(index)
        return redirect('basket:show_basket')

    return HttpResponseRedirect(reverse('category:product_detail', kwargs={'id':pk}))

@login_required(login_url='/customer/login')
def show_basket(request):
    msg = {}

    username = request.session.get('is_login', None)
    if username:
        msg['user'] = username
        msg['logout'] = 'Logout'

    try:
        bsobj = Basket.objects.get(owner__username=username)
    except:
        bsobj = None
    msg['basket'] = bsobj
    return render_to_response('basket/show_basket.html', msg, context_instance=RequestContext(request))

# 删除购物车里面的商品
def remove_product_line(request):

    msg = {'status':0}

    if request.method == 'POST':
        id = request.POST.get('id', None)
        if id == None:
            return redirect(index)

        try:
            lineobj = Line.objects.get(product__id=id)
            lineobj.delete()
        except:
            return redirect(index)
        msg['status'] = 1
        return HttpResponse(json.dumps(msg))

    else:
        return redirect(index)