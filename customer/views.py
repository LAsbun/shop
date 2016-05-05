#!/usr/bin/env python
#coding:utf8

import json

from django.shortcuts import render_to_response, redirect, render
from django.views.generic import TemplateView, RedirectView
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import  authenticate, logout as auth_logout, login as auth_login
from django.template.context import RequestContext
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


from customer.forms import EmailUserCreationForm, UserLoginForm
from customer.mixin import RegisterUserMixin
from category.views import index

from customer.utils import get_right_user
# from customer.models import User
# Create your views here.

class LogOutView(RedirectView):
    url = settings.LOGIN_REDIRECT_URL
    permanent = False

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        response = super(LogOutView, self).get(*args, **kwargs)

        return response


def login(request):

    next_url = request.GET.get('next', None)

    msg = {}
    msg['next_url'] = next_url
    msg['registration_form'] = EmailUserCreationForm()
    if request.method == 'POST':
        nex = request.POST.get('next_url', None)
        # print nex
        form = UserLoginForm(request.POST)
        if form.is_valid():
            accountname = form.cleaned_data['accountname']
            pwd = form.cleaned_data['password']


            # 登陆
            user = get_right_user(accountname, pwd)
            if user:
                auth_login(request, user=user)

            request.session['is_login'] = user.username
            if nex != 'None':

                temp = nex.strip().split('/') #处理next_url
                return HttpResponseRedirect(reverse(temp[2], kwargs={'pk':temp[3]}))
            else:
                return redirect(index)
        else:
            msg['login_form'] = form
            return render_to_response('customer/login_registration.html', msg, context_instance=RequestContext(request))


    msg['login_form'] = UserLoginForm()

    return render_to_response('customer/login_registration.html', msg, context_instance=RequestContext(request))

def registration(request):
    msg = {}
    msg['login_form'] = UserLoginForm()
    if request.method == 'POST':
        # print type(request.POST)
        formss = EmailUserCreationForm(request.POST)

        print formss.is_bound
        if formss.is_valid():
            cleaned_data = formss.cleaned_data
            username = cleaned_data['username']
            email = cleaned_data['email']

            pwd = cleaned_data['password1']
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=pwd)
            user.save()
            request.session['is_login'] = username
            return redirect(index)
        else:
            print 's'
            msg['registration_form'] = formss
            return render_to_response('customer/login_registration.html', msg, context_instance=RequestContext(request))

    msg['registration_form'] = EmailUserCreationForm()


    return render_to_response('customer/login_registration.html', msg, context_instance=RequestContext(request))

def logout(request):
    request.session['is_login'] = None
    auth_logout(request)
    return redirect(index)