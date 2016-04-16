#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

from random import randint

def get_list_randon_int(num, stop=1):
    """
    :param num:  生成num个随机整数
    :return: list
    """
    res = []
    for i in range(num):
        res.append(randint(1, stop))
    return res