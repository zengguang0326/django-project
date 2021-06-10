#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@author:曾光
@file:urls.py
@time:2021/04/20
"""
from django.urls import path
from . import views

urlpatterns = [
    path('',views.IndexView.as_view(),name='index'),
]









