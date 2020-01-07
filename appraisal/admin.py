from django.contrib import admin
from datetime import datetime, date, timedelta

from django.utils.html import format_html

from .models import Devices, Organization, ApplyRecord, ApplyDevice, \
    DeviceStatus, AppraisalType, AppraisalPurpose, BasicInfo, Sample, \
    SampleRecord, AppraisalInfo, FilePhase


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    model = Organization
    list_display = ('name', 'license_num', 'org_id',)


@admin.register(DeviceStatus)
class DeviceStatus(admin.ModelAdmin):
    model = DeviceStatus
    list_display = ('id', 'status',)
    list_display_links = ('id', 'status',)


@admin.register(Devices)
class DevicesAdmin(admin.ModelAdmin):
    model = Devices
    list_display = ('device_id', 'name', 'model', 'detection_department',
                    'detection_period', 'last_detection', 'next_detection', 'status',)
    list_display_links = ('device_id', 'name', 'model',)
    search_fields = ('name', 'model',)
    list_filter = ('status',)
    ordering = ('device_id',)


class ApplyDeviceInline(admin.TabularInline):
    model = ApplyDevice
    extra = 1


@admin.register(ApplyRecord)
class ApplyRecordAdmin(admin.ModelAdmin):
    model = ApplyRecord
    list_display = ('proposer', 'created_time', 'status',)

    inlines = [ApplyDeviceInline]
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
    list_display = ('name', 'org', 'type', 'purpose', 'principal', 'target', 'deadline',)
    search_fields = ('name', 'principal', 'target',)
    list_filter = ('org', 'type', 'purpose',)

    def deadline(self, obj):
        interval = obj.created_date + timedelta(days=30) - date.today()
        if interval.days >= 15:
            color_code = 'green'
        elif 15 > interval.days >= 5:
            color_code = 'orange'
        else:
            color_code = 'red'
            # TODO: 添加居中的样式
        return format_html('<strong><span style="color:{};">{}</span></strong>', color_code, interval.days)

    deadline.short_description = '结束期限'
    deadline.admin_order_field = 'interval.days'


@admin.register(AppraisalInfo)
class AppraisalInfoAdmin(admin.ModelAdmin):
    model = AppraisalInfo
    list_display = ('project_name',)
    filter_horizontal = ('appraisal_team',)
    # 避免下拉菜单太长
    raw_id_fields = ('basic_info',)

    def project_name(self, obj):
        return obj.basic_info.name


@admin.register(FilePhase)
class FilePhaseAdmin(admin.ModelAdmin):
    model = FilePhase
    list_display = ('project_name', 'finished_date', 'file_date',)

    def project_name(self, obj):
        return obj.basic_info.name


@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    model = Sample
    list_display = ('name', 'quantity', 'get_basic_info_name', 'received_date',
                    'receiver',)
    # TODO: 如何将get_basic_info_name加入排序？
    ordering = ('-received_date',)

    def get_basic_info_name(self, obj):
        return obj.basic_info.name


@admin.register(SampleRecord)
class SampleRecordAdmin(admin.ModelAdmin):
    model = SampleRecord
    list_display = ('get_sample_name', 'borrower', 'borrowing_time',
                    'return_time', 'is_returned')

    def get_sample_name(self, obj):
        return obj.sample.name


admin.site.site_header = '山东求是司法鉴定质量管控平台'
admin.site.site_title = '山东求是司法鉴定质量管控平台'
