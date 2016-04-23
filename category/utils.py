#!/usr/bin/env python
#coding:utf-8
__author__ = 'sws'

from django.utils.html import mark_safe
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




class PagiInfo:
    '''
    分页信息
    确定每页有几条信息 per_item
    确定每页的显示开始的信息序号，以及结束序号
    self.Page:当前页
    self.Total_count:信息总数目
    self.Per_item:每页显示的数目 默认为5
    '''

    def __init__(self, page, total_count, per_item=5):
        self.Page = page
        self.Total_count = total_count
        self.Per_item = per_item

    @property
    def start(self):
        '''
        返回开始的序号
        '''
        return self.Per_item*(self.Page-1)

    @property
    def end(self):
        '''
        返回结束的序号
        '''
        return self.Per_item*(self.Page)

    @property
    def total_pages(self):
        '''
            返回总页数
        '''
        pages = divmod(self.Total_count,self.Per_item)
        if pages[1] != 0:
            total_page = pages[0]+1
        else:
            total_page = pages[0]
        return total_page

def Paginor(page, total_pages, url_string):
    '''
    :param page:  当前页
    :param total_pages:  总页数
    :return: 分页字符串
    '''

    # text = lambda x: "{% " + "url 'category/product_list' %s " %(x) + " %}"
    # print text(1)
    if total_pages < 9:
        start = 0
        end = total_pages
    else:
        if page < 5:
            start = 0
            end = 10
        else:
            start = page - 5
            if page + 4 > total_pages:
                end = total_pages
            else:
                end = page+4

    pa_html = ['<a class = "btn btn-default" href="'+url_string+'1">首页</a>']
    if page <= 1:
        pa_html.append('<a class = "btn btn-default" href=#>前一页</a>')
    else:
        pa_html.append('<a class = "btn btn-default" href='+url_string+'%d>前一页</a>' %(page-1))
    for i in range(start+1, end+1):
        temp = '<a class = "btn btn-default"  href='+url_string+'%d>%d</a>' %(i, i)
        pa_html.append(temp)

    if page >= total_pages:
        pa_html.append('<a class = "btn btn-default"  href=#>后一页</a>')
    else:
        pa_html.append('<a class = "btn btn-default"  href='+url_string+'%d>后一页</a>' %(page+1))

    pa_html.append('<a class = "btn btn-default"  href='+url_string+'%d>尾页</a>' %(total_pages))

    page_string=mark_safe(' '.join(pa_html))

    return page_string

def try_int(num, default = 0):
    """
    转换成int
    :param num:
    :param default:
    :return:
    """
    try:
        return int(num)
    except:
        return default

