
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.static import serve
from rest_framework_jwt.views import obtain_jwt_token

from babel.settings import MEDIA_ROOT

from account.views import CustomUsers

urlpatterns = [

    path("users/", CustomUsers.as_view()),
]
