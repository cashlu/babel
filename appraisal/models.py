from django.db import models
from django.utils import timezone

from account.models import CustomUser

STATUS_CHOICE = (
    ('1', '在库'),
    ('2', '出库'),
    # ('3', '借出'),
    # ('4', '维修'),
    # ('5', '检定'),
    # ('6', '其他'),
)


class Organization(models.Model):
    """
    机构
    """

    name = models.CharField(max_length=50, verbose_name='机构名称')
    address = models.CharField(max_length=200, verbose_name='地址')
    legal_personality = models.CharField(max_length=50, verbose_name='法人')
    range_approved = models.TextField(verbose_name='经营范围')
    supervision_1 = models.CharField(max_length=100, null=True, blank=True,
                                     verbose_name='业务主管部门1')
    supervision_2 = models.CharField(max_length=100, null=True, blank=True,
                                     verbose_name='业务主管部门2')
    license_num = models.CharField(max_length=50, verbose_name='执业许可证号')
    bank = models.CharField(max_length=50, verbose_name='开户行名称')
    account = models.CharField(max_length=50, verbose_name='开户行账号')
    org_id = models.CharField(max_length=50, verbose_name='统一社会信用代码')
    contact = models.CharField(max_length=50, verbose_name='联系人')
    phone_1 = models.CharField(max_length=20, verbose_name='联系电话1')
    phone_2 = models.CharField(max_length=20, verbose_name='联系电话2')
    fax = models.CharField(max_length=20, verbose_name='传真')
    complaints_hotline = models.CharField(max_length=20, verbose_name='监督电话')
    email = models.EmailField(verbose_name='邮箱')

    class Meta:
        verbose_name = '机构'
        verbose_name_plural = verbose_name
        ordering = ('id',)

    def __str__(self):
        return self.name


class DeviceStatus(models.Model):
    """
    设备仪器状态表
    """
    status = models.CharField(max_length=20, verbose_name='状态')

    class Meta:
        verbose_name = '设备仪器状态'
        verbose_name_plural = verbose_name
        ordering = ('id',)

    def __str__(self):
        return self.status


class ApplyRecord(models.Model):
    """
    设备仪器出库记录
    """

    STATUS_CHOICE = (
        ('0', '未完成'),
        ('1', '完成'),
    )

    proposer = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING,
                                 verbose_name='申领人')
    comment = models.TextField(null=True, blank=True, verbose_name='备注')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='申领时间')
    is_return = models.BooleanField(default=False, verbose_name='是否归还')
    return_time = models.DateTimeField(null=True, blank=True, verbose_name='归还时间')
    status = models.CharField(max_length=5, choices=STATUS_CHOICE, default=0,
                              verbose_name='状态')

    class Meta:
        verbose_name = '设备仪器申领'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '设备仪器申领记录'

    def delete(self, using=None, keep_parents=False):
        # 如果申请记录被删除，则该记录对应的所有的出库设备状态恢复到在库。
        for item in self.applydevice_set.all():
            item.device.status = 1
            item.device.save()
        return super().delete(using, keep_parents)

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     print('ApplyRecord.save()')
    #     is_done = 1
    #     for item in self.applydevice_set.all():
    #         if item.device.status != '1':
    #             is_done = 0
    #     self.status = is_done
    #     super().save(force_insert, force_update, using, update_fields)


class AvailDevicesManager(models.Manager):
    """
    自定义管理器：查询所有可申领设备。
    """

    def get_queryset(self):
        return super().get_queryset().filter(status=0)


class Devices(models.Model):
    """
    设备仪器
    """

    device_id = models.CharField(max_length=10, verbose_name='设备编号')
    name = models.CharField(max_length=50, verbose_name='设备名称')
    model = models.CharField(max_length=50, verbose_name='规格型号')
    detection_department = models.CharField(max_length=50,
                                            verbose_name='检定机构')
    detection_period = models.IntegerField(verbose_name='检定周期（月）')
    last_detection = models.DateField(verbose_name='上次检定时间')
    next_detection = models.DateField(verbose_name='下次检定时间')
    # status = models.ForeignKey(DeviceStatus, on_delete=models.DO_NOTHING,
    #                            default=1, verbose_name='设备状态')
    status = models.CharField(max_length=5, choices=STATUS_CHOICE, default=1,
                              verbose_name='库存状态')

    # 指定管理器
    objects = models.Manager()
    avail_devices = AvailDevicesManager()

    class Meta:
        verbose_name = '设备仪器'
        verbose_name_plural = verbose_name
        ordering = ('device_id',)

    def __str__(self):
        status_value = ''
        if self.status == '2':
            status_value = ' - 已出库'
        return '{} - {} ({}){}'.format(self.device_id, self.name,
                                       self.model, status_value)


class ApplyDevice(models.Model):
    """
    申领设备表
    """

    # limit_choices_to的判断条件是汉字“在库”，是因为避免修改数据后，字段的id发生变化。
    device = models.ForeignKey(Devices, on_delete=models.DO_NOTHING,
                               # limit_choices_to={'status': '1'},
                               verbose_name='申领设备')
    record = models.ForeignKey(ApplyRecord, on_delete=models.CASCADE,
                               verbose_name='申领表')

    # apply_time = models.DateTimeField(auto_created=True, verbose_name='申领时间')
    # is_return = models.BooleanField(default=False, verbose_name='是否归还')
    # return_time = models.DateTimeField(null=True, blank=True, verbose_name='归还时间')

    class Meta:
        verbose_name = '设备'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '被申领设备'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        print(self.record.is_return)
        if self.record.is_return is False:
            # 将Device表中对应记录的status改为2，代表该设备已出库，其他申领在设备列表中将看不到这个设备。
            self.device.status = 2
            self.device.save()
        else:
            self.device.status = 1
            self.device.save()
        super().save(force_insert, force_update, using, update_fields)

    def delete(self, using=None, keep_parents=False):
        self.device.status = 1
        self.device.save()
        return super().delete(using, keep_parents)


class AppraisalType(models.Model):
    """
    鉴定类别

    建设工程司法鉴定
    建设工程质量鉴定
    建设工程质量鉴定
    电子数据鉴定
    """
    name = models.CharField(max_length=50, verbose_name='鉴定类别')

    class Meta:
        verbose_name = '鉴定类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class AppraisalPurpose(models.Model):
    """
    鉴定用途，案由

    诉讼、调节、保险、仲裁、自检、公共安全
    """
    name = models.CharField(max_length=20, verbose_name='鉴定用途')

    class Meta:
        verbose_name = '鉴定用途'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class BasicInfo(models.Model):
    """
    鉴定项目基础信息
    立项阶段
    """

    name = models.CharField(max_length=50, verbose_name='项目名称')
    sn = models.CharField(max_length=50, verbose_name='鉴定编号')
    org = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True,
                            verbose_name='鉴定机构')
    type = models.ForeignKey(AppraisalType, on_delete=models.SET_NULL, null=True,
                             verbose_name='鉴定类别')
    purpose = models.ForeignKey(AppraisalPurpose, on_delete=models.SET_NULL, null=True,
                                verbose_name='案由/鉴定用途')
    principal = models.CharField(max_length=50, verbose_name='委托人')
    trust_detail = models.TextField(null=True, blank=True, verbose_name='委托事项')
    is_re_appraisal = models.BooleanField(verbose_name='是否重新鉴定')
    target = models.CharField(max_length=50, verbose_name='被鉴定对象')

    class Meta:
        verbose_name = '立项阶段信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name + '立项阶段信息'


class AppraisalInfo(models.Model):
    """
    鉴定阶段
    """

    basic_info = models.ForeignKey(BasicInfo, on_delete=models.CASCADE, verbose_name='基础信息')
    created_date = models.DateField(null=True, blank=True, verbose_name='受理时间')
    appraisal_team = models.ManyToManyField(CustomUser, related_name='appraisal_team',
                                            verbose_name='鉴定人')
    reviewer = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='reviewer',
                                 verbose_name='复核人')
    opinion = models.TextField(null=True, blank=True, verbose_name='主要鉴定意见')
    archivist = models.ForeignKey(CustomUser, related_name='archivist', on_delete=models.DO_NOTHING,
                                  verbose_name='立卷人')
    appraisal_address = models.CharField(max_length=50, verbose_name='鉴定地址')
    project_detail = models.TextField(null=True, blank=True, verbose_name='基本案情')
    contact = models.CharField(max_length=20, null=True, blank=True, verbose_name='联系人')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='联系电话')
    trust_date = models.DateField(null=True, blank=True, verbose_name='委托时间')
    appraisal_date = models.DateField(verbose_name='鉴定时间')
    discuss_date = models.DateField(null=True, blank=True, verbose_name='讨论时间')

    class Meta:
        verbose_name = '鉴定阶段信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.basic_info.name + '鉴定阶段信息'


class FilePhase(models.Model):
    """
    档案阶段
    """

    DELIVERY_CHOICE = (
        (0, '未送达'),
        (1, '邮寄'),
        (2, '专人送达'),
        (3, '自取'),
    )
    basic_info = models.ForeignKey(BasicInfo, on_delete=models.CASCADE,
                                   verbose_name='基础信息')
    finished_date = models.DateField(null=True, blank=True, verbose_name='完成时间')
    file_date = models.DateField(null=True, blank=True, verbose_name='归档日期')
    delivery = models.CharField(max_length=2, choices=DELIVERY_CHOICE,
                                default=0, verbose_name='送达方式')
    amount = models.IntegerField(verbose_name='份数')

    class Meta:
        verbose_name = '档案阶段信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.basic_info.name + '档案阶段信息'


class Sample(models.Model):
    """
    鉴定材料
    """
    basic_info = models.ForeignKey(BasicInfo, on_delete=models.CASCADE,
                                   verbose_name='基本信息')
    appraisal_info = models.ForeignKey(AppraisalInfo, on_delete=models.CASCADE,
                                       verbose_name='鉴定信息')
    name = models.CharField(max_length=50, verbose_name='材料名称')
    quantity = models.IntegerField(verbose_name='数量')
    received_date = models.DateField(verbose_name='接收时间')
    receiver = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING,
                                 verbose_name='接收人')

    class Meta:
        verbose_name = '鉴定材料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class SampleRecord(models.Model):
    """
    鉴定材料借阅记录
    """
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE,
                               verbose_name='材料')
    borrowing_time = models.DateTimeField(default=timezone.now,
                                          verbose_name='借出时间')
    return_time = models.DateTimeField(null=True, blank=True,
                                       verbose_name='归还时间')
    borrower = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING,
                                 verbose_name='借阅人')
    is_returned = models.BooleanField(verbose_name='是否归还')
    comment = models.TextField(verbose_name='备注')

    class Meta:
        verbose_name = '材料借阅记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.sample.name
