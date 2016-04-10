from django.conf.urls import include, url
from django.contrib import admin

import customer.urls as customer_urls
from customer.views import index
urlpatterns = [
    # Examples:
    # url(r'^$', 'shop.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^customer/', include(customer_urls)),
    url(r'^$', index, name="index"),
]
