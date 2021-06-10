#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@author:曾光
@file:urls.py
@time:2021/04/21
"""
from django.urls import path,re_path
from verifications import views
urlpatterns=[
    re_path(r'image_codes/(?P<uuid>[\w-]+)',views.ImageCodeView.as_view()),
    re_path('^sms_codes/(?P<mobile>1[3-9]\d{9})/$',views.SmsCodeView.as_view()),
]










