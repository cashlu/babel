from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.serializers import Serializer
from rest_framework.settings import APISettings

from . import models


# def md5(username):
#     """ 通过MD5算法为每个登录用户生成随机字符串，当做token来用 """
#     import hashlib
#     import time
#
#     ctime = str(time.time())
#     m = hashlib.md5(bytes(username, encoding="utf-8"))
#     m.update(bytes(ctime, encoding="utf-8"))
#     return m.hexdigest()
#
#
# def jwt_response_payload_handler(token, user=None, request=None):
#     """jwt登录成功的返回格式"""
#     return {
#         "msg": "success",
#         "status": 200,
#         "data": {
#             "token": token,
#             "username": user.username,
#         }
#     }


# def jwt_response_payload_error_handler(serializer, request=None):
#     """jwt登陆失败的返回格式"""
#     return {
#         "msg": "用户名或者密码错误",
#         "status": 400,
#         "detail": serializer.errors
#     }


# class AuthView(APIView):
#     # 用户登录请求使用POST方法
#     def post(self, request, *args, **kwargs):
#         ret = {
#             "code": 1000,
#             "token": None,
#             "msg": None,
#         }
#         try:
#             # 注意使用了drf后，request的获取方式
#             username = request._request.POST.get("username")
#             password = request._request.POST.get("password")
#             user_obj = models.UserInfo.objects.filter(username=username, password=password).first()
#             if not user_obj:
#                 ret["code"] = 1001
#                 ret["msg"] = "用户名或密码错误"
#
#             # 为登录用创建token
#             token = md5(username)
#             # 检查Token表，如果存在现有用户的数据，就update，否则create
#             models.Token.objects.update_or_create(user=user_obj, defaults={"token": token})
#             ret["token"] = token
#             ret["msg"] = "验证通过"
#         except Exception as e:
#             ret["code"] = 1002
#             ret["msg"] = "请求异常"
#
#         return JsonResponse(ret)

# class Test(APIView):
#     def get(self, request, *args, **kwargs):
#         # 下面三个一样
#         print(request.query_params)
#         print(request._request.GET)
#         print(request.GET)
#         return Response("DRF GET OK")
#
#     def post(self, request, *args, **kwargs):
#         # 下面三个一样
#         print(request.data)
#         print(request.POST)
#         print(request._request.POST)
#         return Response("DRF POST OK")


class CustomUsers(APIView):
    def get(self, request, *args, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION")
        # print(request.META.get("HTTP_AUTHORIZATION"))
        # token = request.META.get("HTTP_TOKEN")
        print(token)
        return HttpResponse("ok")