#coding:utf-8
from datetime import datetime

from django.shortcuts import render_to_response
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
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
        # msg['product_list'] = map(get_product, list(bsobj.all_lines()))
        # print msg['product_list'][0].image.url
        msg['quantity'] = quantity
        msg['basket'] = bsobj
        return render_to_response('basket/show_basket.html', msg)
    return HttpResponseRedirect(reverse('category:product_detail', kwargs={'id':pk}))


def get_product(line):
    return Product.objects.get(id=line.product.id)