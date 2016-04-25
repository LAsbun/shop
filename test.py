#!/usr/bin/env python
# encoding: utf-8
# LAsbun  @ 2016-04-24

def application(env, start_response):
        start_response('200 OK', [('Content-Type','text/html')])
        return ["Hello World"]
