#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@author:曾光
@file:urls.py
@time:2021/05/25
"""
from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r'^gitee/$',views.GiteeView.as_view()),
    re_path(r'^oauth_callback/$',views.GiteeCallBackView.as_view()),
]










