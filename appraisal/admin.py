from django.contrib import admin

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
                    'detection_period', 'last_detection', 'next_detection',
                    )

    list_display_links = ('device_id', 'name',)
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
    list_display = ('name', 'org', 'type', 'purpose', 'principal', 'target',)
    # filter_horizontal = ('appraisal_team',)


@admin.register(AppraisalInfo)
class AppraisalInfoAdmin(admin.ModelAdmin):
    model = AppraisalInfo
    list_display = ('project_name', 'created_date',)
    filter_horizontal = ('appraisal_team',)

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
