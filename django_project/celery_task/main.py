#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@author:曾光
@file:main.py
@time:2021/05/06
"""
# Celery程序入口

from celery import Celery

# 为celery使用django配置文件进行设置
import os
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'django_project.settings.dev'

# 创建celery实例
celery_app = Celery('django_project')

# 引入celery中间人配置
celery_app.config_from_object('celery_task.config')

# 注册任务
celery_app.autodiscover_tasks(['celery_task.sms','celery_task.email'])













