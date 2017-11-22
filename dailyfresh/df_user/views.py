# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import JsonResponse ,HttpResponseRedirect
from hashlib import sha1
from models import User,ReceiveInfo
from islogin import islogin

# Create your views here.


#最初进入注册页
def register(request):
    return render(request, 'df_user/register.html')

# 接收注册页面传递的参数，并保存数据
def register_handle(request):

    #获取前端传递的数据
    user_name = request.POST['user_name']
    user_passwd = request.POST['user_passwd']
    user_passwd_again = request.POST['user_passwd_again']
    user_email = request.POST['user_email']
    #print  'user_name:' +  user_name + ', user_passwd: '+ user_passwd +', user_passwd_again:' + user_passwd_again + ',user_email: '+user_email

    #验证两次的密码是否一致
    if user_passwd != user_passwd_again:
        return redirect('/user/register')

    # 对密码进行加密
    s1 = sha1()
    s1.update(user_passwd)
    passwd = s1.hexdigest()

    # 向数据库中写入用户数据
    user = User()
    user.user_name = user_name
    user.user_passwd = passwd
    user.user_email = user_email
    user.save()

    context = {'userinfo' : user}
    return redirect('/user/login')

# 用于检查用户名是否被注册
def user_check(request):
    user_name = request.GET['user_name']
    count = User.objects.filter(user_name=user_name).count()
    context = {'count': count}
    return JsonResponse(context)


# 跳到登录界面
def login(request):
    user_name = request.POST.get('user_name', '')
    context = {'error_username':0, 'error_passwd':0 , 'user_name':user_name}
    return render(request, 'df_user/login.html', context)


# 用于检查登录的用户名与密码是否正确
def login_handle(request):

    # 获取前端传过来的数据
    user_name = request.POST.get('user_name')
    user_passwd = request.POST.get('user_passwd')
    remember = request.POST.get('remember', '0')
    # print request.POST
    # print 'zhao'
    # print user_name
    # print user_passwd
    # print remember
    # print 'yan'
    # 利用前端传过来的用户名从数据库中读取用户对象
    user_info = User.objects.filter(user_name=user_name)

    # 验证用户的密码
    if len(user_info) != 0:

        # 对密码进行加密，
        s1 = sha1()
        s1.update(user_passwd)
        passwd = s1.hexdigest()

        # 密码正确的情况，有个问题，为什么设置了cookie还有去设置session了？？
        if passwd == user_info[0].user_passwd:
            req = HttpResponseRedirect('/user/info/')
            if remember != 0:
                req.set_cookie('user_name', user_name)
            else:
                req.set_cookie('user_name', '', max_age=-1)
            request.session['user_id'] = user_info[0].id
            request.session['user_name'] = user_name

            return req
        # 密码不正确的
        else :
            context = { 'error_username': 0, 'error_passwd': 1, 'user_name': user_name }
            return render(request, 'df_user/login.html', context)

    else:
        context = {'error_username':1, 'error_passwd':0 , 'user_name':user_name}
        return render(request, 'df_user/login.html', context)


# 用户登录中心
@islogin
def info(request):

    # 获取用户信息
    user = User.objects.get(id = request.session['user_id'])

    context = {"user_name" : request.session['user_name'],
               "user_phone" : user.user_phone,
               "user_addr" : user.user_addr}

    return render(request, 'df_user/userinfo.html', context)


# 用户收获地址，
@islogin
def get_user_receive_addr(request):
    # 根据用户的ID获取用户保存的收获地址
    user = User.objects.get(id = request.session['user_id'])
    address = user.receiveinfo_set.all()
    context ={'address' : address}
    for addr in address:
        print addr.receive_name , addr.receive_addr, addr.receive_phone

    return render(request, 'df_user/addrinfo.html', context)


# 添加收获地址信息
@islogin
def add_user_receive_addr(request):
    new_user_name = request.POST['receive_name']
    new_user_phone = request.POST['receive_phone']
    new_user_addr = request.POST['receive_addr']
    user_id = request.session['user_id']

    