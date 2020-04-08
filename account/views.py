from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from rest_framework.utils import json


@csrf_exempt
def login(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")
        if username is not None and password is not None:
            is_login = authenticate(request, username=username, password=password)
            if is_login:
                return JsonResponse({
                    "data": {},
                    "meta": {
                        "status": 200,
                        "message": "Login Success",
                    }
                })
            else:
                return JsonResponse({
                    "data": {},
                    "meta": {
                        "status": "403",
                        "message": "Login Failed"
                    }
                })
