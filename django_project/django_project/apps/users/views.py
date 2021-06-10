from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http.response import JsonResponse,HttpResponse,HttpResponseForbidden
from django.db import DatabaseError
from django.contrib.auth import login,authenticate,logout
from django_redis import get_redis_connection
import logging
import re,json
from django import http
from users.models import User
from django_project.utils.response_code import RETCODE
from django.contrib.auth.mixins import LoginRequiredMixin
from django_project.utils.utils_loginrequiredmixin import LoginRequiredJsonMixin
# Create your views here.


# 用户需要先登录
class EmailView(LoginRequiredJsonMixin, View):
    """修改用户邮箱接口"""
    def put(self, request):
        # 接收参数
        # json_str = request.body
        # json_str = json_str.decode()  # python3.6 无需执行此步
        # req_data = json.loads(json_str)
        email = json.loads(request.body).get('email')
        # 校验参数
        if not email:
            return HttpResponseForbidden('缺少email参数')
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return HttpResponseForbidden('参数email有误')
        # 修改用户邮箱信息
        user = request.user
        try:
            user.email = email
            user.save()
        except Exception as e:
            logging.error(e)
            return JsonResponse({'code': RETCODE.DBERR, 'errmsg': '添加邮箱失败'})

        # 响应添加邮箱结果
        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': '添加邮箱成功'})

class UserCenterInfoView(LoginRequiredMixin, View):
    """用户中心信息"""
    def get(self,request):
        # login_url 在settings 指定
        # redirect_field_name  默认next
        # 如果通过了loginRequedMixin验证,则可以通过request.user 获取当前登录的用户信息
        context={
            'username':request.user.username,
            'mobile':request.user.mobile,
            'email':request.user.email,
            'email_active':request.user.email_active,
        }
        return render(request,'user_center_info.html', context)


class LogoutView(View):
    def get(self, request):
        # 清除状态保持
        logout(request)
        # 返回响应 重定向到登录页
        resp = redirect(reverse('users:login'))
        # 删除保存cookie
        resp.delete_cookie('username')
        # 返回响应
        return resp


class LoginView(View):
    def get(self,request):
        """定义登录视图"""
        return render(request,'login.html')

    def post(self,request):
        # 接收参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')
        # 校验参数
        # 判断参数是否齐全
        if not all([username, password]):
            return HttpResponseForbidden('缺少必传参数')

        # 判断用户名是否是5-20个字符
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return HttpResponseForbidden('请输入正确的用户名或手机号')

        # 判断密码是否是8-20个数字
        if not re.match(r'^[0-9A-Za-z]{8,20}$', password):
            return HttpResponseForbidden('密码最少8位，最长20位')
        # 验证用户是否存在
        # django 默认方法不满足需求，重写authenticate
        user = authenticate(username=username,password=password)

        if user is None:
            # 如果用户不存在,返回登录页
            return render(request,'login.html',{'error_msg':'用户名或密码错误'})
        # 状态保持
        login(request,user)
        # 判断是否记住密码
        if remembered != 'on':
            # 0为关闭浏览器就结束会话
            request.session.set_expiry(0)
        else:
            # 默认保存两周
            request.session.set_expiry(None)

        # 返回响应，
        next = request.GET.get('next')
        if next:
            # 如果获取到next,跳转到对应路径
            resp = redirect(next)
        else:
            # 否则重定向到首页
            resp = redirect(reverse('contents:index'))
        # 将响应值设置cookie
        resp.set_cookie('username',user.username,max_age=60*60*24*1)
        # 返回响应
        return resp


class UsernameCountView(View):
    """定义查询用户名数量视图"""
    def get(self,request,username):
        """
        :param request: 请求对象
        :param username: 用户名
        :return: Json
        """
        try:
            count = User.objects.filter(username=username).count()
        except Exception as e:
            logging.error(e)
            return JsonResponse({'code':RETCODE.DBERR,'errmsg':'查询错误','count':-1})
        return JsonResponse({'code':RETCODE.OK,'errmsg':'OK','count':count})


class MobileCountView(View):
    def get(self,request,mobile):
        """
        根据手机号查询注册数量
        :param request:
        :param mobile:
        :return: json
        """
        count = User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code':RETCODE.OK,'errmsg':'OK','count':count})


class RegisterView(View):
    """用户注册 注册成功跳转登录页"""

    def get(self,request):
        """
        提供注册界面

        :param request: 请求对象
        :return: 注册界面
        """

        return render(request,'register.html')

    def post(self,request):

        # 接收参数
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        sms_code_client = request.POST.get('sms_code')
        allow = request.POST.get('allow')

        # 校验参数
        if not all([username,password,password2,mobile,allow]):
            return HttpResponseForbidden('参数不完整')
        # 校验用户名
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$',username):
            return HttpResponseForbidden('请输入5-20个字符的用户名')
        # 校验密码
        if not re.match(r'^[a-zA-Z0-9_-]{8,20}$',password):
            return HttpResponseForbidden('请输入8-20位的密码')
        # 校验确认密码
        if password != password2:
            return HttpResponseForbidden('两次输入的密码不一致')
        # 校验手机号
        if not re.match(r'^1[3-9]\d{9}$',mobile):
            return HttpResponseForbidden('输入的手机号格式不正确')
        # 校验验证码
        # 创建redis连接对象
        redis_conn = get_redis_connection('verify')
        # 获取验证码
        sms_code_server = redis_conn.get('sms_code_%s' % mobile)
        # 删除验证码
        redis_conn.delete('sms_code_%s' % mobile)
        if sms_code_server is None:
            return render(request, 'register.html', {'sms_code_errmsg': '短信验证码失效'})
        # 对比验证码
        if sms_code_client != sms_code_server.decode():
            return render(request,'register.html',{'register_errmsg': '输入短信验证码有误'})
        # 校验allow
        if allow != 'on':
            return HttpResponseForbidden('用户协议未勾选')
        # 保存数据
        try:
            user = User.objects.create_user(username=username,password=password,mobile=mobile)
        except DatabaseError:
            # 数据库异常返回注册页面
            return render(request,'register.html',{'register_errmsg': '注册失败'})
        # 注册成功之后进行登录保持
        # login(request,user)

        # 返回响应
        # return HttpResponse(request,{'name':"aaa"})
        # return HttpResponse('注册成功，重定向到首页')
        # pass
        # 返回响应，重定向到首页
        # resp = redirect(reverse('contents:index'))
        # 返回响应，重定向到登录页
        # resp = redirect(reverse('users:login'))
        # # 将响应值设置cookie
        # resp.set_cookie('username', user.username, max_age=60 * 60 * 24 * 1)
        # return resp
        # 返回响应，重定向到登录页
        return redirect(reverse('users:login'))