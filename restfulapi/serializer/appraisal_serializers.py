from rest_framework import serializers
from rest_framework.relations import RelatedField, PrimaryKeyRelatedField

from appraisal.models import Organization, DeviceStatus, ApplyRecord, \
    Devices, AppraisalType, AppraisalPurpose, BasicInfo, \
    AppraisalInfo, FilePhase, AppraisalFile, AppraisalFileRecord, \
    AppraisalSample, LocaleFile, AdditionalFile, CustomUser, TodoList, \
    AppraisalFileImage, LocaleFileImage, DeliveryState, AddiFileImage, CheckRecord, DeviceGroup, \
    ApplyRecordDetail, ApplyPurpose

from django.contrib.auth.models import Group

from restfulapi.models import Menus


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = "__all__"
        depth = 3


class DeviceStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceStatus
        fields = "__all__"


class ApplyRecordSerializer(serializers.ModelSerializer):
    proposer_name = serializers.CharField(source="proposer.name", read_only=True)

    class Meta:
        model = ApplyRecord
        fields = "__all__"


class ApplyRecordDetailSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source="device.name", read_only=True)
    device_id = serializers.CharField(source="device.device_id", read_only=True)
    proposer_name = serializers.CharField(source="apply_record.proposer.name", read_only=True)

    class Meta:
        model = ApplyRecordDetail
        fields = "__all__"


class ApplyPurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyPurpose
        fields = "__all__"


class DevicesSerializer(serializers.ModelSerializer):
    status_name = serializers.PrimaryKeyRelatedField(source="status.name", read_only=True)

    class Meta:
        model = Devices
        fields = "__all__"


class DeviceGroupSerializer(serializers.ModelSerializer):
    devices = DevicesSerializer(many=True)

    class Meta:
        model = DeviceGroup
        fields = "__all__"
        # depth = 3


class AppraisalTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppraisalType
        fields = "__all__"
        depth = 0


class AppraisalPurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppraisalPurpose
        fields = "__all__"
        depth = 1


class BasicInfoSerializer(serializers.ModelSerializer):
    """
    基础信息的序列化器。
    单独指定了三个外键关联的关系型字段。把这三个字段一起传给前端，前端就可以直接获取到关联的数据，
    而不需要再次发起请求来获取别的类的数据了。

    这里没有使用depth，因为depth虽然方便，但是有副作用，所有嵌套的数据，是不能修改的。
    """
    # org，type，purpose三个是外键，默认只获得了ID，我们希望还能获得name字段
    org_name = PrimaryKeyRelatedField(source='org.name', read_only=True)
    type_name = PrimaryKeyRelatedField(source='type.name', read_only=True)
    purpose_name = PrimaryKeyRelatedField(source='purpose.name', read_only=True)
    creator_name = PrimaryKeyRelatedField(source='creator.name', read_only=True)
    reviewer_name = PrimaryKeyRelatedField(source="reviewer.name", read_only=True)
    # appr_info = serializers.CharField(source='appr_info.id', read_only=True)
    # 获取项目对应的ApprInfo
    proofreader = serializers.PrimaryKeyRelatedField(source='appr_info.proofreader', read_only=True)
    final_reviewer = serializers.PrimaryKeyRelatedField(source='appr_info.final_reviewer', read_only=True)

    class Meta:
        model = BasicInfo
        fields = "__all__"


class BasicDetailInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BasicInfo
        fields = "__all__"
        # depth = 1


class CheckRecordSerializer(serializers.ModelSerializer):
    basicInfo_name = PrimaryKeyRelatedField(source="basicInfo.name", read_only=True)
    basicInfo_sn = PrimaryKeyRelatedField(source="basicInfo.sn", read_only=True)
    reviewer_name = PrimaryKeyRelatedField(source="reviewer.name", read_only=True)
    status_text = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = CheckRecord
        # fields = ["basicInfo", "basicInfo_name", "opinion", "reviewer", "reviewer_name",
        #           "created_date", "status", "basicInfo_sn", "type"]
        fields = "__all__"


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class ApprInfoSerializer(serializers.ModelSerializer):
    basic_info_sn = PrimaryKeyRelatedField(source="basic_info.sn", read_only=True)
    basic_info_name = PrimaryKeyRelatedField(source="basic_info.name", read_only=True)
    basic_info_stage = PrimaryKeyRelatedField(source="basic_info.stage", read_only=True)
    archivist_name = PrimaryKeyRelatedField(source="archivist.name", read_only=True)
    final_reviewer_name = PrimaryKeyRelatedField(source="final_reviewer.name", read_only=True)
    proofreader_name = PrimaryKeyRelatedField(source="proofreader.name", read_only=True)
    # 如果使用下面的写法，那么传给前端的就是对象数组，可以轻松的获取对象的各个属性，用来渲染页面，
    # 但是，同样的，前端发来的POST请求，这个数组也必须是对象数组，比较麻烦
    # appraisal_team = CustomUserSerializer(many=True)
    appraisal_team = PrimaryKeyRelatedField(many=True, queryset=CustomUser.objects.all())

    # def create(self, validated_data):
    #     team = validated_data.pop("appraisal_team")
    #     info_obj = AppraisalInfo.objects.create(**validated_data)
    #     for p in team:
    #         person = CustomUser.objects.get(pk=p)
    #         info_obj.appraisal_team.add(p)
    #     return info_obj

    # def update(self, instance, validated_data):
    #     pass

    class Meta:
        model = AppraisalInfo
        # fields = "__all__"
        fields = ["id", "basic_info", "appraisal_team", "final_reviewer", "proofreader", "opinion",
                  "archivist", "appraisal_address", "project_detail", "contact",
                  "phone", "appraisal_date", "discuss_date", "basic_info_sn", "basic_info_stage",
                  "basic_info_name", "archivist_name", "final_reviewer_name", "proofreader_name",
                  "appraisal_team"]


# class ApprInfoSerializerL(serializers.ModelSerializer):
#     class Meta:
#         model = AppraisalInfo
#         fields = "__all__"
#         depth = 1
#
#
# class ApprInfoSerializerLCDUR(serializers.ModelSerializer):
#     appraisal_team = serializers.ListField()
#
#     # appraisal_team = PrimaryKeyRelatedField(many=True,
#     #                                         queryset=CustomUser.objects.all())
#
#     class Meta:
#         model = AppraisalInfo
#         fields = "__all__"
#
#     # 重写了create方法，因为需要通过前端传过来的数据，
#     # 向AppraisalInfo实例中添加关联的appraisal_team
#     def create(self, validated_data):
#         print(validated_data)
#         team_persons = validated_data.pop("appraisal_team")[0].split(",")
#         print(team_persons)
#         info_obj = AppraisalInfo.objects.create(**validated_data)
#         for p_id in team_persons:
#             person = CustomUser.objects.get(pk=p_id)
#             # TODO: 这里用了add方法，再试一下set方法
#             info_obj.appraisal_team.add(person)
#         return info_obj
#
#     # FIXME: update方法还没重写，是否需要？
#     # def update(self, instance, validated_data):
#     #     # update方法是否对应的是put请求？
#     #     pass


# class ApprlInfoSerializer(serializers.Serializer):
#     basic_info = BasicInfoSerializer(required=True)
#     appraisal_team = CustomUserSerializer(required=True, many=True)
#     reviewer = CustomUserSerializer(required=True)
#     opinion = serializers.CharField(required=True)
#     archivist = CustomUserSerializer(required=True)
#     appraisal_address = serializers.CharField(required=True)
#     project_detail = serializers.CharField(required=True)
#     contact = serializers.CharField(required=True)
#     phone = serializers.CharField(required=True)
#     appraisal_date = serializers.DateField(required=True)
#     discuss_date = serializers.DateField(required=True)


class AppraisalFileSerializer(serializers.ModelSerializer):
    basic_info_sn = PrimaryKeyRelatedField(source="basic_info.sn", read_only=True)
    basic_info_name = PrimaryKeyRelatedField(source="basic_info.name", read_only=True)
    basic_info_stage = PrimaryKeyRelatedField(source="basic_info.stage", read_only=True)
    receiver_name = PrimaryKeyRelatedField(source="receiver.name", read_only=True)
    images = PrimaryKeyRelatedField(many=True, required=False,
                                    queryset=AppraisalFileImage.objects.all())

    is_available = serializers.SerializerMethodField()
    borrower = serializers.SerializerMethodField()
    last_record = serializers.SerializerMethodField()

    def get_is_available(self, obj):
        record = obj.records.last()
        if not record:
            return True
        elif record.is_returned:
            return True
        else:
            return False

    def get_borrower(self, obj):
        record = obj.records.last()
        if not record:
            return None
        if not record.is_returned:
            return record.borrower.id

    def get_last_record(self, obj):
        record = obj.records.last()
        if not record:
            return None
        if record.is_returned:
            return None
        else:
            return record.id

    class Meta:
        model = AppraisalFile
        fields = "__all__"


class AppraisalFileImageSerializer(serializers.ModelSerializer):
    # TODO: 这句貌似没用，如果测试有报错，优先查这一句
    # appr_file = PrimaryKeyRelatedField(source="appraisal_file", read_only=True)

    class Meta:
        model = AppraisalFileImage
        fields = "__all__"


class AppraisalFileRecordSerializer(serializers.ModelSerializer):
    borrower_name = PrimaryKeyRelatedField(source="borrower.name", read_only=True)
    appr_file_name = PrimaryKeyRelatedField(source="appraisal_file.name", read_only=True)

    class Meta:
        model = AppraisalFileRecord
        fields = "__all__"


class LocaleFileSerializer(serializers.ModelSerializer):
    basic_info_name = PrimaryKeyRelatedField(source="basic_info.name", read_only=True)
    basic_info_stage = PrimaryKeyRelatedField(source="basic_info.stage", read_only=True)
    images = PrimaryKeyRelatedField(many=True, required=False,
                                    queryset=LocaleFileImage.objects.all())

    class Meta:
        model = LocaleFile
        fields = "__all__"


class LocaleFileImageSerializer(serializers.ModelSerializer):
    # TODO：为什么下面这句会报错，而在AppraisalFileImageSerializer中不报错？
    # locale_file = PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = LocaleFileImage
        fields = "__all__"


class AppraisalSampleSerializer(serializers.ModelSerializer):
    basic_info_name = serializers.PrimaryKeyRelatedField(source="basic_info.name", read_only=True)
    basic_info_stage = serializers.PrimaryKeyRelatedField(source="basic_info.stage", read_only=True)
    receiver_name = serializers.PrimaryKeyRelatedField(source="receiver.name", read_only=True)

    class Meta:
        model = AppraisalSample
        fields = "__all__"


class DeliveryStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryState
        fields = "__all__"


class FilePhaseSerializer(serializers.ModelSerializer):
    basic_info_name = serializers.PrimaryKeyRelatedField(source="basic_info.name", read_only=True)
    delivery_text = serializers.CharField(source="delivery.name", read_only=True)

    class Meta:
        model = FilePhase
        fields = "__all__"


class AddiFileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddiFileImage
        fields = "__all__"


class AdditionalFileSerializer(serializers.ModelSerializer):
    basic_info_name = serializers.PrimaryKeyRelatedField(source="basic_info.name", read_only=True)
    images = serializers.PrimaryKeyRelatedField(many=True, required=False,
                                                queryset=AddiFileImage.objects.all())

    class Meta:
        model = AdditionalFile
        fields = "__all__"


class TodoListSerializer(serializers.ModelSerializer):
    basic_info_name = serializers.PrimaryKeyRelatedField(source="basic_info.name", read_only=True)
    basic_info_sn = serializers.PrimaryKeyRelatedField(source="basic_info.sn", read_only=True)
    user_name = serializers.PrimaryKeyRelatedField(source="user.name", read_only=True)
    type_text = serializers.CharField(source="get_type_display", read_only=True)

    class Meta:
        model = TodoList
        fields = "__all__"


# 终于搞定了外键自关联关系，反向关联的数据获取！！！！！！！！！
# TODO： 注释了下面的三个depth，大幅缩短了获取菜单的时间，观察是否有Bug
class MenusSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Menus
        fields = "__all__"
        # depth = 3


class MenusSerializer(serializers.ModelSerializer):
    # subMenu这个字段的名称，必须和model中related_name一致。
    subMenu = MenusSerializer2(many=True)

    class Meta:
        model = Menus
        fields = "__all__"
        # depth = 3


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
        # depth = 3


# class FileDataSerializer(serializers.Serializer):
#     typename = serializers.CharField()
#     sn = serializers.CharField()
#     purpose = serializers.CharField()
#     principal = serializers.CharField()
#     trust_detail = serializers.CharField()
#     is_re_appraisal = serializers.CharField()
#     target = serializers.CharField()
#     created_date = serializers.DateField()
#     finished_date = serializers.DateField()
#     appraisal_team = serializers.ListField()
#     final_reviewer = serializers.CharField()
#     opinion = serializers.CharField()
#     archivist = serializers.CharField()
#     file_date = serializers.CharField()
#     appraisal_address = serializers.CharField()
#     project_detail = serializers.CharField()
#     delivery = serializers.CharField()
#     contact = serializers.CharField()
#     phone = serializers.CharField()
