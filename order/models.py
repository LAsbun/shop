#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

from django.contrib.auth.models import User
from django.db import models


from basket.models import Basket
from customer.abstract_models import AbstractAddress
# 订单
class Order(models.Model):

    number = models.CharField(
        max_length=128,db_index=True,unique=True,
        verbose_name='订单号'
    )

    basket = models.ForeignKey(
        Basket, null=True, blank=True, on_delete=models.SET_NULL,
        verbose_name='购物车'
    )

    user = models.ForeignKey(
        User, related_name='orders', null=True, blank=True,
        on_delete=models.SET_NULL,
        verbose_name='用户'
    )

    billing_address = models.ForeignKey(
        BillingAddress, null=True,blank=True,
        on_delete=models.SET_NULL,
        verbose_name='支付地址'
    )

    shipping_tax = models.DecimalField(
        decimal_places=2, max_digits=12,
        default=0,
        verbose_name='邮费'
    )

    shipping_address = models.ForeignKey(
        ShippingAddress, null=True, blank=True,
        verbose_name='送货地址'
    )

    shipping_method = models.CharField(
        max_length=128,blank=True,
        verbose_name='送货方式'
    )

    status = models.CharField(
        blank=True, default="",
        verbose_name='订单状态'
    )

    def __unicode__(self):
        return self.number

    class Meta:
        verbose_name_plural = verbose_name = '订单'




class BillingAddress(AbstractAddress):
    class Meta:
        app_label = 'order'
        verbose_name = '支付地址'
        verbose_name_plural = '支付地址'

    @property
    def order(self):
        """
        Return the order linked to this shipping address
        """
        try:
            return self.order_set.all()[0]
        except IndexError:
            return None


class ShippingAddress(AbstractAddress):
    phone_number = models.CharField(
        '手机号', blank=True,

        )
    notes = models.TextField(
        blank=True,
        verbose_name='备注',

        )

    class Meta:
        abstract = True
        # ShippingAddress is registered in order/models.py
        app_label = 'order'
        verbose_name = '送货地址'
        verbose_name_plural = '送货地址'

    @property
    def order(self):
        """
        Return the order linked to this shipping address
        """
        try:
            return self.order_set.all()[0]
        except IndexError:
            return None