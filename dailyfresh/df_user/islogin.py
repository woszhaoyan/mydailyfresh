#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/22 16:42
# @Author  : zhaoyan
# @File    : islogin.py

from django.http import HttpResponseRedirect

#如果登录则转到登录页面
def islogin(func):
    def login_fun(request, *args, **kwargs):
        user_id = request.session.get('user_id', '')
        if user_id :
            return func(request, *args, **kwargs)
        else:
            red = HttpResponseRedirect('/user/login/')
            #  了解一下request.get_full_path是干嘛，下面这句话的作用
            print  request.get_full_path
            red.set_cookie('url', request.get_full_path)
            return red

    return login_fun