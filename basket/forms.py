#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

from django import forms


class AddToBasketForm(forms.Form):
    quantity = forms.IntegerField(initial=1, min_value=1, label="数量")

    def __init__(self, basket, product, *args, **kwargs):
        # Note, the product passed in here isn't necessarily the product being
        # added to the basket. For child products, it is the *parent* product
        # that gets passed to the form. An optional product_id param is passed
        # to indicate the ID of the child product being added to the basket.
        self.basket = basket
        self.product = product

        super(AddToBasketForm, self).__init__(*args, **kwargs)

    def clean_quantity(self):
        # Check that the proposed new line quantity is sensible
        qty = self.cleaned_data['quantity']

        if qty > self.product.store_count:
            raise forms.ValidationError(
                '超过库存量'
            )

        return qty


