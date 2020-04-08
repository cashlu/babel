import json

from django.contrib.auth.models import Group
from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, ListCreateAPIView, GenericAPIView
from rest_framework import viewsets, mixins
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin, \
    RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import IsAdminUser, IsAuthenticated, DjangoModelPermissions
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from account.models import CustomUser
from appraisal.models import Organization, DeviceStatus, ApplyRecord, Devices, \
    AppraisalType, AppraisalPurpose, BasicInfo, AppraisalInfo, \
    FilePhase, AppraisalFile, AppraisalFileRecord, AppraisalSample, LocaleFile, \
    AdditionalFile, AppraisalFileImage, LocaleFileImage, DeliveryState, AddiFileImage
from .serializer.account_serializers import CustomUserSerializer
from .serializer.appraisal_serializers import \
    OrganizationSerializer, DeviceStatusSerializer, ApplyRecordSerializer, \
    DevicesSerializer, AppraisalTypeSerializer, \
    AppraisalPurposeSerializer, BasicInfoSerializer, \
    FilePhaseSerializer, AppraisalFileSerializer, AppraisalFileRecordSerializer, \
    AppraisalSampleSerializer, LocaleFileSerializer, AdditionalFileSerializer, MenusSerializer, \
    GroupSerializer, BasicDetailInfoSerializer, ApprInfoSerializer, AppraisalFileImageSerializer, \
    LocaleFileImageSerializer, DeliveryStateSerializer, AddiFileImageSerializer

from .models import Menus

from rest_framework.pagination import PageNumberPagination


# TODO: 这个类要换地方
class CustomPagination(PageNumberPagination):
    page_size = 5
    page_query_param = 'page'
    page_size_query_param = 'size'


class CustomUserView(viewsets.ModelViewSet):
    serializer_class = CustomUserSerializer
    queryset = CustomUser.objects.all()


class OrganizationView(viewsets.ModelViewSet):
    serializer_class = OrganizationSerializer
    queryset = Organization.objects.all().order_by("name")


class DeviceStatusView(viewsets.ModelViewSet):
    serializer_class = DeviceStatusSerializer
    queryset = DeviceStatus.objects.all()


class ApplyRecordView(viewsets.ModelViewSet):
    serializer_class = ApplyRecordSerializer
    queryset = ApplyRecord.objects.all()


class DevicesView(viewsets.ModelViewSet):
    serializer_class = DevicesSerializer

    # queryset = Devices.objects.all()
    def get_queryset(self):
        paginator = self.request.query_params.get("paginator")
        if paginator:
            self.pagination_class = CustomPagination
        return Devices.objects.all().order_by("device_id")


class AppraisalTypeView(viewsets.ModelViewSet):
    serializer_class = AppraisalTypeSerializer
    queryset = AppraisalType.objects.all()


class AppraisalPurposeView(viewsets.ModelViewSet):
    serializer_class = AppraisalPurposeSerializer
    queryset = AppraisalPurpose.objects.all()


class BasicInfoView(ModelViewSet):
    """
    项目基础信息
    """
    serializer_class = BasicInfoSerializer

    # permission_classes = (DjangoModelPermissions,)

    def get_queryset(self):
        stage = self.request.query_params.get("stage")
        paginator = self.request.query_params.get("paginator")

        # 是否需要分页(只有项目列表需要分页，并且要获取所有阶段的数据)
        if paginator == "true":
            self.pagination_class = CustomPagination

        # 是否需要指定stage（其他地方都是在下拉框中使用，所以不分页，不过要区分阶段）
        if stage:
            return BasicInfo.objects.filter(stage=stage).order_by("-id")
        else:
            return BasicInfo.objects.all().order_by("-id")


# class ApprInfoView(APIView):
#     """
#     鉴定信息维护的View。
#     """
#
#     def get(self, request, *args, **kwargs):
#         """
#         用于获取一个或多个AppraisalInfo记录。
#         :param request: DRF封装的Request对象。
#         :param args: 位置参数。
#         :param kwargs: 具名参数，主要是为了获取PK值。
#         :return: Response对象，返回前端请求的具体数据和状态。
#         """
#         # 获取AppraisalInfo列表，需要分页
#         if not kwargs.get("pk"):
#             queryset = AppraisalInfo.objects.all().order_by("-id")
#             count = queryset.count()
#             # 分页
#             pg = CustomPagination()
#             page_queryset = pg.paginate_queryset(queryset=queryset, request=request, view=self)
#             serializer = ApprInfoSerializerNew(page_queryset, many=True)
#             ret = {
#                 "status": status.HTTP_200_OK,
#                 "msg": "获取鉴定信息列表成功",
#                 "data": serializer.data,
#                 "count": count
#             }
#             return Response(ret)
#         # 具有pk参数，查询的是一个对象，不需要分页
#         else:
#             pk = kwargs.get("pk")
#             queryset = get_object_or_404(AppraisalInfo, pk=pk)
#             serializer = ApprInfoSerializerNew(instance=queryset, many=False)
#             ret = {
#                 "status": status.HTTP_200_OK,
#                 "msg": "获取鉴定信息成功",
#                 "data": serializer.data,
#                 "count": 1
#             }
#             return Response(ret)
#
#     def post(self, request, *args, **kwargs):
#         serializer = ApprInfoSerializerNew(data=request.data, many=False)
#         if serializer.is_valid():
#             serializer.save()
#             ret = {
#                 "status": status.HTTP_201_CREATED,
#                 "msg": "创建项目信息成功"
#             }
#             return Response(ret)
#         ret = {
#             "status": status.HTTP_400_BAD_REQUEST,
#             "msg": "添加项目信息失败",
#             "error": serializer.errors,
#         }
#         print(serializer.errors)
#         return Response(ret)
#
#     def put(self, request, *args, **kwargs):
#         pk = kwargs.get("pk")
#         if pk:
#             obj = get_object_or_404(AppraisalInfo, pk=pk)
#             serializer = ApprInfoSerializerNew(data=request.data, instance=obj)
#             if serializer.is_valid():
#                 serializer.save()
#                 ret = {
#                     "status": status.HTTP_200_OK,
#                     "msg": "信息更新成功"
#                 }
#                 return Response(ret)
#             ret = {
#                 "status": status.HTTP_400_BAD_REQUEST,
#                 "msg": "信息更新失败in"
#             }
#             return Response(ret)
#         else:
#             ret = {
#                 "status": status.HTTP_400_BAD_REQUEST,
#                 "msg": "信息更新失败"
#             }
#             return Response(ret)
#
#     def delete(self, request, *args, **kwargs):
#         pk = kwargs.get("pk")
#         if pk:
#             obj = AppraisalInfo.objects.get(pk=pk)
#             obj.delete()
#             ret = {
#                 "status": status.HTTP_200_OK,
#                 "msg": "记录删除成功"
#             }
#             return Response(ret)
#         ret = {
#             "status": status.HTTP_400_BAD_REQUEST,
#             "msg": "删除请求失败，请联系管理员"
#         }
#         return Response(ret)

class ApprInfoView(ModelViewSet):
    """
    鉴定信息
    """
    serializer_class = ApprInfoSerializer
    permission_classes = (DjangoModelPermissions,)

    def get_queryset(self):
        paginator = self.request.query_params.get("paginator")

        if paginator == "true":
            self.pagination_class = CustomPagination
        return AppraisalInfo.objects.all().order_by("-id")


class AppraisalFileView(viewsets.ModelViewSet):
    serializer_class = AppraisalFileSerializer
    # 如果要使用分页，那么queryset要排序
    queryset = AppraisalFile.objects.all().order_by("-id")
    pagination_class = CustomPagination


class AppraisalFileImageView(viewsets.ModelViewSet):
    serializer_class = AppraisalFileImageSerializer

    def get_queryset(self):
        appr_info_id = self.request.query_params.get("id")
        if appr_info_id:
            return AppraisalFileImage.objects.filter(appraisal_file_id=appr_info_id)
        else:
            return AppraisalFileImage.objects.all()


class LocaleFileView(viewsets.ModelViewSet):
    serializer_class = LocaleFileSerializer
    queryset = LocaleFile.objects.all().order_by("-id")
    pagination_class = CustomPagination


class LocaleFileImageView(viewsets.ModelViewSet):
    serializer_class = LocaleFileImageSerializer

    def get_queryset(self):
        locale_file_id = self.request.query_params.get("id")
        if locale_file_id:
            return LocaleFileImage.objects.filter(locale_file_id=locale_file_id)
        else:
            return LocaleFileImage.objects.all()


class AppraisalFileRecordView(viewsets.ModelViewSet):
    serializer_class = AppraisalFileRecordSerializer
    queryset = AppraisalFileRecord.objects.all().order_by("-id")
    pagination_class = CustomPagination


class AppraisalSampleView(viewsets.ModelViewSet):
    serializer_class = AppraisalSampleSerializer
    queryset = AppraisalSample.objects.all().order_by("-id")
    pagination_class = CustomPagination


class DeliveryStateView(viewsets.ModelViewSet):
    serializer_class = DeliveryStateSerializer
    queryset = DeliveryState.objects.all()


class FilePhaseView(viewsets.ModelViewSet):
    serializer_class = FilePhaseSerializer
    queryset = FilePhase.objects.all().order_by("-id")
    pagination_class = CustomPagination


class AddiFileImageView(viewsets.ModelViewSet):
    serializer_class = AddiFileImageSerializer

    def get_queryset(self):
        addi_file_id = self.request.query_params.get("id")
        if addi_file_id:
            return AddiFileImage.objects.filter(addiFile=addi_file_id)
        else:
            return AddiFileImage.objects.all()


class AdditionalFileView(viewsets.ModelViewSet):
    serializer_class = AdditionalFileSerializer
    queryset = AdditionalFile.objects.all().order_by("-id")
    pagination_class = CustomPagination


# FIXME: 改造为ModelViewSet
class MenusView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        user = request.user
        groups = Group.objects.filter(user=user)

        menu_id_list = []
        for group in groups:
            for item in group.group_menus.all():
                menu_id_list.append(item.menu_id)
        items = Menus.objects.filter(level=1, menu_id__in=menu_id_list)
        ser = MenusSerializer(instance=items, many=True)
        ret = {
            "status": 200,
            "data": ser.data,
        }
        return Response(ret)
