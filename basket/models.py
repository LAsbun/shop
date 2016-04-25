#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import PermissionDenied

from category.models import Product

# 购物车
class Basket(models.Model):

    owner = models.ForeignKey(
        User, related_name='baskets', null=True,
        verbose_name= '拥有者'
    )

    OPEN, MERGED, SAVED, FROZEN, SUBMITTED = (
        "Open", "Merged", "Saved", "Frozen", "Submitted")
    STATUS_CHOICES = (
        (OPEN, _("Open - currently active")),
        (MERGED, _("Merged - superceded by another basket")),
        (SAVED, _("Saved - for items to be purchased later")),
        (FROZEN, _("Frozen - the basket cannot be modified")),
        (SUBMITTED, _("Submitted - has been ordered at the checkout")),
    )

    status = models.CharField(
        choices=STATUS_CHOICES, max_length=128, default=OPEN,
        verbose_name='交易状态'
    )

    date_create = models.DateTimeField(
        verbose_name='添加时间'
    )

    date_submitted = models.DateTimeField(
        '下单时间',
        null=True,
        blank=True
    )

    editable_statuses = (OPEN, SAVED)

    class Meta:
        verbose_name_plural = verbose_name = '购物车'

    def __init__(self, *args, **kwargs):
        super(Basket, self).__init__(*args, **kwargs)

        # We keep a cached copy of the basket lines as we refer to them often
        # within the same request cycle.  Also, applying offers will append
        # discount data to the basket lines which isn't persisted to the DB and
        # so we want to avoid reloading them as this would drop the discount
        # information.
        self._lines = None


    def __unicode__(self):
        return _(
            u"%(status)s basket (owner: %(owner)s, lines: %(num_lines)d)") \
               % {'status': self.status,
                  'owner': self.owner,
                  'num_lines': self.num_lines}

    def all_lines(self):
        """
        返回原来cache购物车中所有的的商品
        """
        if self.id is None:
            return self.lines.none()
        if self._lines is None:
            self._lines = (
                self.lines
                    .select_related('product', )
                    .prefetch_related(
                    'attributes', 'product__images'))
        return self._lines

    @property
    def num_lines(self):
        return self.all_lines().count()


    @property
    def can_be_edited(self):
        """
        验证是否可以编辑
        """
        return self.status in self.editable_statuses

# 交易单
class Line(models.Model):


    basket = models.ForeignKey(
        Basket, related_name='lines',
        verbose_name='购物车'
    )

    product = models.ForeignKey(
        Product, related_name='basket_lines',
        verbose_name= '商品'
    )

    quantity = models.PositiveIntegerField(
        default=1,verbose_name='数量'
    )

    date_create = models.DateTimeField(
        auto_now_add=True, verbose_name='创建时间'
    )


    class Meta:
        verbose_name_plural = verbose_name = '购物商品行'


    def __unicode__(self):
        return _(
            u"Basket #%(basket_id)d, Product #%(product_id)d, quantity"
            u" %(quantity)d") % {'basket_id': self.basket.pk,
                                 'product_id': self.product.pk,
                                 'quantity': self.quantity}


    def save(self, *args, **kwargs):
        if not self.basket.can_be_edited:
            raise PermissionDenied(
                _("You cannot modify a %s basket") % (
                    self.basket.status.lower(),))
        return super(Line, self).save(*args, **kwargs)