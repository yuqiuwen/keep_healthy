import json
import random
import datetime
import os, sys
import traceback
import ast
import json
from logger import logger

from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.db.transaction import atomic
from django.http import HttpResponse, JsonResponse, request
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

from .models import User
from common.http_response import HttpResponse
from .models import User
from .serializers import UserModelSerializer
from celery_tasks.send_email import tasks
from utils.common import *




class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer

    @action(methods=['POST'], detail=False)
    def login(self, request):
        try:
            username = request.data.get('username')
            email = request.data.get('email')
            password = request.data.get('password')
            user = authenticate(request, username=username, password=password, email=email)
            if not user or user.email != email:
                logger.error('用户{}登录异常'.format(username))
                return HttpResponse.response_failed('信息不正确,请检查')

            old_token = Token.objects.filter(user=user)
            old_token.delete()
            login(request, user)
            token = Token.objects.create(user=user)
            logger.info('用户{}登录成功'.format(username))
            res = {
                'token': token.key,
                'role': user.roles,
                'username': user.username,
                'user': user.id,
                'sex': user.sex
            }
            return HttpResponse.response_success('登录成功', res)

        except Exception as e:
            error = traceback.format_exc(limit=3)
            logger.error(error)
            return HttpResponse.response_failed(error)

    @action(methods=['POST'], detail=False)
    def logout(self, request):
        try:
            logout(request)
            return HttpResponse.response_success('退出登录成功')
        except Exception as e:
            return HttpResponse.response_failed('退出登录失败')

    @action(methods=['POST'], detail=False)
    def send_email(self, request):
        try:
            email = request.data.get('email')
            username = request.data.get('username')
            query = User.objects.filter(email=email)
            if query:
                return HttpResponse.response_failed('邮箱号已存在')
            code = random.sample([str(i) for i in range(10)], 6)  # 从list中随机获取6个元素，作为一个片断返回
            verification_code = ''.join(code)
            res = tasks.send_mail_code.apply_async(kwargs={
                'email': email,
                'user': username,
                'code': verification_code})
            res.get()
            if not res.status:
                return HttpResponse.response_failed('发送失败')

            return HttpResponse.response_success('发送成功', res.id)

        # except User.DoesNotExist:
        #     return HttpResponse.response_failed('该邮箱号已注册')
        except Exception as e:
            logger.error(traceback.format_exc(limit=3))
            return HttpResponse.response_failed('发送失败')



    @action(methods=['POST'], detail=False)
    def register(self, request):
        try:
            res = {'user': None, 'msg': None}

            username = request.data.get('username')
            mail = request.data.get('email')
            task_id = request.data.get('task_id')
            code = request.data.get('verifyCode')
            password = request.data.get('password')
            remember = request.data.get('is_remember')
            now = datetime.datetime.now()
            user = User.objects.filter(username=username)
            if not task_id:
                return HttpResponse.response_failed('task_id不能为空')
            if user:
                return HttpResponse.response_failed('用户已存在')
            print(task_id, mail, code)
            sql = f"""select task_id, date_created, status, task_kwargs from django_celery_results_taskresult where task_id = %s"""
            query = query_all(sql, [task_id, ])[0]
            task_kwargs = ast.literal_eval(json.loads(query["task_kwargs"]))

            if (now - query['date_created']).seconds > 600 * 5:
                return HttpResponse.response_failed('验证码失效')
            print(task_kwargs,task_kwargs['code'])
            if str(task_kwargs['code']) == str(code):
                User.objects.create_user(username=username, password=password, email=mail, is_remember=remember, sex='F', roles=0)
                new_user = authenticate(request, username=username, password=password, email=mail)
                token = Token.objects.create(user=new_user)
                login(request, new_user)
                res = {
                    'token': token.key,
                    'role': new_user.roles,
                    'username': new_user.username,
                    'user': new_user.id,
                    'sex': new_user.sex
                }
            else:
                return HttpResponse.response_success('验证码错误')

            return HttpResponse.response_success('注册成功', res)
        except Exception as e:
            logger.error(traceback.format_exc(limit=3))
            return HttpResponse.response_failed('注册失败')

    def gen_verify_email_url(self, user):
        """
        生成邮箱激活链接
        @param user: 当前登录用户
        @return: token
        """
        pass
    def check_user_info(self, mail):
        pass


