from django.contrib import admin
from datetime import datetime, date, timedelta

from django.utils.html import format_html
from django.utils.safestring import mark_safe

from .models import Devices, Organization, ApplyRecord, CheckRecord, \
    DeviceStatus, AppraisalType, AppraisalPurpose, BasicInfo, AppraisalFile, \
    AppraisalFileRecord, AppraisalInfo, FilePhase, AppraisalSample, LocaleFile, \
    AdditionalFile, AppraisalFileImage, LocaleFileImage, DeliveryState, AddiFileImage, \
    TodoList


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    list_display = ('name', 'license_num', 'org_id',)


@admin.register(DeviceStatus)
class DeviceStatus(admin.ModelAdmin):
    model = DeviceStatus
    list_display = ('id', 'code', 'name',)
    list_display_links = ('id', 'code', 'name',)


@admin.register(Devices)
class DevicesAdmin(admin.ModelAdmin):
    model = Devices
    list_display = ('device_id', 'name', 'model', 'detection_department',
                    'detection_period', 'last_detection', 'status',)
    list_display_links = ('device_id', 'name', 'model',)
    search_fields = ('name', 'model',)
    list_filter = ('status',)
    ordering = ('device_id',)


# class ApplyDeviceInline(admin.TabularInline):
#     model = ApplyDevice
#     extra = 1


@admin.register(ApplyRecord)
class ApplyRecordAdmin(admin.ModelAdmin):
    model = ApplyRecord
    list_display = ('proposer', 'applied_time', 'comment')

    # inlines = [ApplyDeviceInline]
    readonly_fields = ('proposer',)

    def save_model(self, request, obj, form, change):
        # 保存时自动写入当前登录用户，不能手工修改。
        obj.proposer = request.user

        # 如果选中了“是否归还”的复选框，则将对应的借出设备的状态重置为“在库”，否则，置为“出库”
        if obj.is_return:
            for item in obj.applydevice_set.all():
                item.device.status = 1
                item.device.save()
        else:
            for item in obj.applydevice_set.all():
                item.device.status = 2
                item.device.save()
        super().save_model(request, obj, form, change)


@admin.register(AppraisalType)
class AppraisalTypeAdmin(admin.ModelAdmin):
    model = AppraisalType
    list_display = ('id', 'name',)


@admin.register(AppraisalPurpose)
class AppraisalPurposeAdmin(admin.ModelAdmin):
    model = AppraisalPurpose
    list_display = ('id', 'name',)


@admin.register(BasicInfo)
class BasicInfoAdmin(admin.ModelAdmin):
    model = BasicInfo
    list_display = ('name', 'org', 'type', 'purpose', 'principal', 'target', 'creator', 'deadline',)
    search_fields = ('name', 'principal', 'target',)
    list_filter = ('org', 'type', 'purpose',)

    def deadline(self, obj):
        interval = obj.created_date + timedelta(days=30) - date.today()
        # 这里超期显示负数可能更好一些
        # interval_days = interval.days if interval.days >= 0 else 0

        if interval.days >= 15:
            color_code = 'green'
        elif 15 > interval.days >= 5:
            color_code = 'orange'
        else:
            color_code = 'red'
        return format_html('<strong><span style="background-color:{};'
                           'text-align:center;display:inline-block;width:50px">{}</span></strong>',
                           color_code, str(interval.days) + '天')

    deadline.short_description = '结束期限'
    deadline.admin_order_field = 'interval.days'


@admin.register(CheckRecord)
class CheckRecordAdmin(admin.ModelAdmin):
    model = CheckRecord
    list_display = ("basicInfo", "reviewer", "created_date", "status",)


@admin.register(AppraisalInfo)
class AppraisalInfoAdmin(admin.ModelAdmin):
    model = AppraisalInfo
    list_display = ('project_name',)
    filter_horizontal = ('appraisal_team',)
    # 避免下拉菜单太长
    raw_id_fields = ('basic_info',)

    def project_name(self, obj):
        return obj.basic_info.name


@admin.register(DeliveryState)
class DeliveryStateAdmin(admin.ModelAdmin):
    model = DeliveryState
    list_display = ("code", "name",)


@admin.register(FilePhase)
class FilePhaseAdmin(admin.ModelAdmin):
    model = FilePhase
    list_display = ('project_name', 'finished_date', 'file_date',)

    def project_name(self, obj):
        return obj.basic_info.name


@admin.register(AppraisalFile)
class AppraisalFileAdmin(admin.ModelAdmin):
    model = AppraisalFile
    list_display = ('name', 'quantity', 'get_basic_info_name', 'received_date',
                    'receiver',)
    ordering = ('-received_date',)

    def get_basic_info_name(self, obj):
        return obj.basic_info.name

    get_basic_info_name.short_description = '项目名称'


@admin.register(AppraisalFileImage)
class ApprsaisalFileImageAdmin(admin.ModelAdmin):
    model = AppraisalFileImage
    list_display = ('file',)


@admin.register(AppraisalFileRecord)
class SampleRecordAdmin(admin.ModelAdmin):
    model = AppraisalFileRecord
    list_display = ('borrower', 'borrowing_time',
                    'return_time', 'is_returned')


@admin.register(AppraisalSample)
class AppraisalSampleAdmin(admin.ModelAdmin):
    model = AppraisalSample
    list_display = ('name', 'quantity', 'get_basic_info_name', 'received_date',
                    'receiver',)
    ordering = ('-received_date',)

    def get_basic_info_name(self, obj):
        return obj.basic_info.name

    get_basic_info_name.short_description = '项目名称'


@admin.register(LocaleFile)
class LocaleFileAdmin(admin.ModelAdmin):
    model = LocaleFile
    list_display = ('name', 'basic_info', 'created_date',)
    list_display_links = ('name', 'basic_info',)
    ordering = ('-basic_info', '-created_date',)
    search_fields = ('name', 'basic_info',)


@admin.register(LocaleFileImage)
class LocaleFileImageAdmin(admin.ModelAdmin):
    model = LocaleFileImage
    list_display = ("id", "locale_file", "file",)


@admin.register(AdditionalFile)
class AdditionalFileAdmin(admin.ModelAdmin):
    model = AdditionalFile
    list_display = ('name', 'basic_info', 'created_date',)
    list_display_links = ('name', 'basic_info',)
    ordering = ('-basic_info', '-created_date',)

    search_fields = ('name', 'basic_info',)


@admin.register(AddiFileImage)
class AddiFileImageAdmin(admin.ModelAdmin):
    model = AddiFileImage
    list_display = ("addiFile", "file",)


@admin.register(TodoList)
class TodoListAdmin(admin.ModelAdmin):
    model = TodoList
    list_display = ("basic_info", "get_basic_info_name", "get_user_name", "type", "created_time", "finished")

    def get_basic_info_name(self, obj):
        return obj.basic_info.name

    def get_user_name(self, obj):
        return obj.user.name

    get_basic_info_name.short_description = '项目名称'
    get_user_name.short_description = "处理用户"


admin.site.site_header = '山东求是司法鉴定质量管控平台'
admin.site.site_title = '山东求是司法鉴定质量管控平台'
