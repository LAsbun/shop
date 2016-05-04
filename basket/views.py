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

@login_required(login_url='/customer/login')
def add_to_basket(request, pk):
    msg = {}

    if request.method == 'POST':
        user = request.session['is_login']
        quantity = request.POST.get('quantity', 1)
        print quantity, user
        try:

            bsobj = Basket.objects.create(owner=User.objects.get(username=user))
            bsobj.save()
            print bsobj.can_be_edited
            lineonj = Line.objects.create(basket=bsobj, product=Product.objects.get(id=pk), quantity=int(quantity), date_create=datetime.now())
            print lineonj

            print 'ss'
            lineonj.save()
        except Exception, e:
            print e
            return redirect(index)
        msg['product'] = lineonj.product
        msg['quantity'] = quantity
        return render_to_response('basket/show_basket.html', msg)
    return HttpResponseRedirect(reverse('category:product_detail', kwargs={'id':pk}))