#!/usr/bin/env python
# coding:utf-8
from django.conf.urls import include, url, static
from django.contrib import admin
from django.conf import settings

import customer.urls as customer_urls
from category.views import index
from shop.upload import upload_image
import category.urls as category_url
import basket.urls as basket_url

urlpatterns = [
    # Examples:
    # url(r'^$', 'shop.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url

    url(r'uploads/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root':settings.MEDIA_ROOT,}),
    url(r'^admin/upload/(?P<dir_name>[^/]+)$',
        upload_image,name='upload_image'),

    url(r'^admin/', include(admin.site.urls)),
     # 购物车
    url(r'^basket/', include(basket_url, namespace='basket')),
    # 登录注册相关
    url(r'^customer/', include(customer_urls, namespace='customer')),
    # 分类，产品相关
    url(r'^category/', include(category_url, namespace='category')),

    # 首页
    url(r'^$', index, name="index"),
]

# urlpatterns += static(settings.MEDIA_URL, {'document_root':settings.MEDIA_ROOT,})