#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@author:曾光
@file:urls.py
@time:2021/04/15
"""
from django.urls import path , include,re_path
from . import views

# 解决Specifying a namespace in include() without providing an app_name is not supported. Set the app_name attribute in the included module, or pass a 2-tuple containing the list of patterns and app_name instead.报错
# app_name='users'

urlpatterns = [
    # 匹配正则的时候可以用re_path
    # re_path(r'^register/$',views.RegisterView.as_view(),name='register'),
    path('register/',views.RegisterView.as_view(),name='register'),
    re_path(r'usernames/(?P<username>[a-zA-Z0-9_-]{5,20})/count/',views.UsernameCountView.as_view()),
    re_path(r'mobiles/(?P<mobile>1[3-9]\d{9})/count',views.MobileCountView.as_view()),
    re_path(r'login/',views.LoginView.as_view(),name='login'),
    re_path(r'logout/',views.LogoutView.as_view(),name='logout'),
    re_path(r'^info/$',views.UserCenterInfoView.as_view(),name='info'),
    re_path(r'^emails/$',views.EmailView.as_view()),


]











