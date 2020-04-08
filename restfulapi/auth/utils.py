from django.contrib.auth.middleware import get_user
from django.utils.functional import SimpleLazyObject
from rest_framework.permissions import SAFE_METHODS
from rest_framework.renderers import BaseRenderer, JSONRenderer
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from account.models import CustomUser
from django.contrib.auth.models import Group, Permission, AnonymousUser


def jwt_response_payload_handler(token, user=None, request=None):
    """
    jwt登录认证成功返回的数据
    :param token: 返回的jwt
    :param user: 当前登录的用户对象
    :param request: 客户端提交的request请求数据
    :return: 返回包含token，userID，username的字典
    """

    groups = Group.objects.filter(user=user)
    permissions = []
    for group in groups:
        permission = Permission.objects.filter(group=group.pk)
        permissions.append(permission)
    # print(user.username)
    # print(groups)
    # print(permissions)
    return {
        "status": 200,
        "token": token,
        "id": user.id,
        "username": user.username,
        # "groups": groups,
        # "permissions": permissions,
    }


def jwt_response_payload_error_handler(serializer, request=None):
    """
    jwt登录认证失败返回的数据
    :param serializer: 序列化对象
    :param request: 发送的登录请求request
    :return: 包含错误信息和状态码的字典
    """
    print("失败")
    return {
        "msg": "用户名或者密码错误",
        "status": 401,
        "detail": serializer.errors
    }


# class JSONWebTokenAuthenticationInSafeMETHODS(JSONWebTokenAuthentication):
#     def get_jwt_value(self,request):
#         """
#         重写JWT认证，如果是SAFE_METHODS直接跳过
#         :param request:
#         :return:
#         """
#         if request.method in SAFE_METHODS:
#             return None
#         return super().get_jwt_value(request)

# 解决request.user是Anonymous的问题的中间件。
def get_user_jwt(request):
    """
    Replacement for django session auth get_user & auth.get_user
     JSON Web Token authentication. Inspects the token for the user_id,
     attempts to get that user from the DB & assigns the user on the
     request object. Otherwise it defaults to AnonymousUser.

    This will work with existing decorators like LoginRequired  ;)

    Returns: instance of user object or AnonymousUser object
    """
    user = None
    try:
        user_jwt = JSONWebTokenAuthentication().authenticate(Request(request))
        if user_jwt is not None:
            # store the first part from the tuple (user, obj)
            user = user_jwt[0]
    except:
        pass

    return user or AnonymousUser()


class JWTAuthenticationMiddleware(object):
    """ Middleware for authenticating JSON Web Tokens in Authorize Header """
    def process_request(self, request):
        request.user = SimpleLazyObject(lambda : get_user_jwt(request))



