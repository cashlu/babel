from django.contrib.auth.models import Group
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.views import APIView
from rest_framework.response import Response

from account.models import CustomUser
from appraisal.models import Organization, DeviceStatus, ApplyRecord, Devices, \
    AppraisalType, AppraisalPurpose, BasicInfo, AppraisalInfo, \
    FilePhase, AppraisalFile, AppraisalFileRecord, AppraisalSample, LocaleFile, \
    AdditionalFile, AppraisalFileImage, LocaleFileImage, DeliveryState, AddiFileImage, CheckRecord, TodoList, \
    ApplyRecordDetail, DeviceGroup
from .serializer.account_serializers import CustomUserSerializer
from .serializer.appraisal_serializers import OrganizationSerializer, DeviceStatusSerializer, ApplyRecordSerializer, \
    DevicesSerializer, AppraisalTypeSerializer, AppraisalPurposeSerializer, BasicInfoSerializer, \
    FilePhaseSerializer, AppraisalFileSerializer, AppraisalFileRecordSerializer, \
    AppraisalSampleSerializer, LocaleFileSerializer, AdditionalFileSerializer, MenusSerializer, \
    ApprInfoSerializer, AppraisalFileImageSerializer, LocaleFileImageSerializer, DeliveryStateSerializer, \
    AddiFileImageSerializer, CheckRecordSerializer, TodoListSerializer, DeviceGroupSerializer, \
    ApplyRecordDetailSerializer

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


class ApplyRecordDetailView(viewsets.ModelViewSet):
    serializer_class = ApplyRecordDetailSerializer

    # queryset = ApplyRecordDetail.objects.all()
    def get_queryset(self):
        device_id = self.request.query_params.get("deviceId")
        if device_id:
            return ApplyRecordDetail.objects.filter(device=device_id, is_returned=False).order_by("-id")
        return ApplyRecordDetail.objects.all().order_by("-id")


class DeviceGroupView(viewsets.ModelViewSet):
    serializer_class = DeviceGroupSerializer
    queryset = DeviceGroup.objects.all()


class DevicesView(viewsets.ModelViewSet):
    serializer_class = DevicesSerializer

    # queryset = Devices.objects.all()
    def get_queryset(self):
        paginator = self.request.query_params.get("paginator")
        status = self.request.query_params.get("status")
        if paginator:
            self.pagination_class = CustomPagination
        if status:
            return Devices.objects.filter(status=status).order_by("group")
        return Devices.objects.all().order_by("group")


class AppraisalTypeView(viewsets.ModelViewSet):
    serializer_class = AppraisalTypeSerializer
    queryset = AppraisalType.objects.all()


class AppraisalPurposeView(viewsets.ModelViewSet):
    serializer_class = AppraisalPurposeSerializer
    queryset = AppraisalPurpose.objects.all()


class BasicInfoView(viewsets.ModelViewSet):
    """
    项目基础信息
    """
    serializer_class = BasicInfoSerializer

    # permission_classes = (DjangoModelPermissions,)

    # def get_queryset(self):
    #     stage = self.request.query_params.get("stage")
    #     paginator = self.request.query_params.get("paginator")
    #     query = self.request.query_params.get("query")
    #
    #     # 是否需要分页(只有项目列表需要分页，并且要获取所有阶段的数据)
    #     if paginator == "true":
    #         self.pagination_class = CustomPagination
    #
    #     if query == "one":
    #         return BasicInfo.objects.all()
    #
    #     # 获取基础信息列表的时候，需要指定所处阶段
    #     if stage == '0':
    #         return BasicInfo.objects.all().order_by("-id")
    #     return BasicInfo.objects.filter(stage=stage).order_by("-id")

    def get_queryset(self):
        stage = self.request.query_params.get("stage")
        paginator = self.request.query_params.get("paginator")
        can_apply_device = self.request.query_params.get("canApplyDevice")

        # 是否需要分页(只有项目列表需要分页，并且要获取所有阶段的数据)
        if paginator == "true":
            self.pagination_class = CustomPagination

        # 获取基础信息列表的时候，需要指定所处阶段
        if stage:
            return BasicInfo.objects.filter(stage=stage).order_by("-id")

        if can_apply_device:
            # 立项审批后，立卷前的项目，可以申领设备
            return BasicInfo.objects.filter(stage__in=[4, 5, 6]).order_by("-id")
        return BasicInfo.objects.all().order_by("-id")


class CheckRecordView(viewsets.ModelViewSet):
    """
    审批记录
    """

    serializer_class = CheckRecordSerializer
    # queryset = BasicInfoReviews.objects.all().order_by("-id")
    pagination_class = CustomPagination
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        query = self.request.query_params.get("query")
        paginator = self.request.query_params.get("paginator")
        basic_info_id = self.request.query_params.get("basic_info_id")
        type = self.request.query_params.get("type")

        if paginator == "true":
            self.pagination_class = CustomPagination

        # 有两个可选条件，分别为basic_info_id,和type
        if basic_info_id and type:
            return CheckRecord.objects.filter(basicInfo_id=basic_info_id, type=type).order_by("-id")
        elif basic_info_id:
            return CheckRecord.objects.filter(basicInfo_id=basic_info_id).order_by("-id")
        elif type:
            return CheckRecord.objects.filter(type=type).order_by("-id")
        return CheckRecord.objects.all().order_by("-id")


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

class ApprInfoView(viewsets.ModelViewSet):
    """
    鉴定信息
    """
    serializer_class = ApprInfoSerializer
    permission_classes = (DjangoModelPermissions,)

    def get_queryset(self):
        paginator = self.request.query_params.get("paginator")
        basic_info_id = self.request.query_params.get("basicInfoId")
        if basic_info_id:
            return AppraisalInfo.objects.filter(basic_info_id=basic_info_id).order_by("-id")
        if paginator == "true":
            self.pagination_class = CustomPagination
        return AppraisalInfo.objects.all().order_by("-id")


class AppraisalFileView(viewsets.ModelViewSet):
    serializer_class = AppraisalFileSerializer
    # 如果要使用分页，那么queryset要排序
    # queryset = AppraisalFile.objects.all().order_by("-id")
    pagination_class = CustomPagination

    def get_queryset(self):
        basic_info_id = self.request.query_params.get("basic_info")
        if basic_info_id:
            return AppraisalFile.objects.filter(basic_info_id=basic_info_id).order_by("-id")
        return AppraisalFile.objects.all().order_by("-id")


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
    # queryset = LocaleFile.objects.all().order_by("-id")
    pagination_class = CustomPagination

    def get_queryset(self):
        basic_info_id = self.request.query_params.get("id")
        if basic_info_id:
            return LocaleFile.objects.filter(basic_info_id=basic_info_id).order_by("-id")
        return LocaleFile.objects.all().order_by("-id")


class LocaleFileImageView(viewsets.ModelViewSet):
    serializer_class = LocaleFileImageSerializer

    def get_queryset(self):
        locale_file_id = self.request.query_params.get("id")
        if locale_file_id:
            return LocaleFileImage.objects.filter(locale_file_id=locale_file_id).order_by("-id")
        else:
            return LocaleFileImage.objects.all().order_by("-id")


class AppraisalFileRecordView(viewsets.ModelViewSet):
    serializer_class = AppraisalFileRecordSerializer

    # queryset = AppraisalFileRecord.objects.all().order_by("-id")

    def get_queryset(self):
        apprfile = self.request.query_params.get("apprFileId")
        if apprfile:
            return AppraisalFileRecord.objects.filter(appraisal_file=apprfile).order_by("-id")
        else:
            pagination_class = CustomPagination
            return AppraisalFileRecord.objects.all().order_by("-id")


class AppraisalSampleView(viewsets.ModelViewSet):
    serializer_class = AppraisalSampleSerializer

    # pagination_class = CustomPagination

    def get_queryset(self):
        basic_info_id = self.request.query_params.get("id")
        if basic_info_id:
            return AppraisalSample.objects.filter(basic_info_id=basic_info_id).order_by("-id")
        return AppraisalSample.objects.all().order_by("-id")


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


class TodoListView(viewsets.ModelViewSet):
    serializer_class = TodoListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        basic_info_id = self.request.query_params.get("basic_info")
        user = self.request.query_params.get("user")
        is_finished = self.request.query_params.get("is_finished")

        if basic_info_id:
            return TodoList.objects.filter(basic_info=basic_info_id).order_by("-id")
        else:
            if is_finished == "true" and user:
                return TodoList.objects.filter(user=user, finished=True).order_by("-id")
            elif is_finished == "false" and user:
                return TodoList.objects.filter(user=user, finished=False).order_by("-id")
            elif is_finished == "true" and not user:
                return TodoList.objects.filter(finished=True).order_by("-id")
            elif is_finished == "false" and not user:
                return TodoList.objects.filter(finished=False).order_by("-id")
            else:
                return TodoList.objects.all().order_by("-id")


# class MenusView(APIView):
#     permission_classes = (IsAuthenticated,)
#
#     def get(self, request):
#         token = request.META.get("HTTP_AUTHORIZATION")
#         user = request.user
#         groups = Group.objects.filter(user=user)
#         menu_id_list = []
#         for group in groups:
#             for item in group.group_menus.all():
#                 menu_id_list.append(item.menu_id)
#         items = Menus.objects.filter(level=1, menu_id__in=menu_id_list)
#         ser = MenusSerializer(instance=items, many=True)
#         ret = {
#             "status": 200,
#             "data": ser.data,
#         }
#         return Response(ret)

class MenusView(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    serializer_class = MenusSerializer

    def get_queryset(self):
        user = self.request.user
        groups = Group.objects.filter(user=user)
        menu_id_list = []
        for group in groups:
            for item in group.group_menus.all():
                menu_id_list.append(item.menu_id)
        menu_id_list = set(menu_id_list)
        return Menus.objects.filter(level=1, menu_id__in=menu_id_list)
