#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@author:曾光
@file:tasks.py
@time:2021/05/06
"""
# 创建异步任务
from celery_task.main import celery_app

from celery_task.sms.ronglian_sms.SendMessage import SMS
from . import constants

@celery_app.task
def send_sms_code(mobile,sms_code):
    """
    创建异步发送短信任务
    :param mobile: 手机号
    :param sms_code: 短信验证码
    :return: 成功 0 , 失败 -1
    """
    result = SMS().send_message(constants.SEND_SMS_TEMPLATE_ID, mobile, (sms_code, constants.SMS_CODE_REDIS_EXPIRES // 60))
    return result









