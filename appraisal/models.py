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
    # SN_TYPE_CHOICE = (('1', '建'), ('2', '声'), ('3', '像'), ('4', '电'),)
    # SN_PURPOSE = (('1', '鉴'), ('2', '检'),)

    STAGE_CHOICE = (('1', '立项中'),  # 立项信息暂存，没有提交
                    ('2', '立项提交'),  # 立项信息提交，进入立项审批环节
                    ('3', '立项审批中'),  # 立项信息审批中，没有提交
                    ('4', '立项审批通过'),  # 立项信息审批通过，可以进行后续操作
                    ('5', '立卷中'),  # 鉴定信息暂存，没有提交
                    ('6', '立卷提交'),  # 鉴定信息已提交，进入校对环节
                    ('7', '校对中'),  # 校对暂存，没有提交
                    ('8', '校对提交'),  # 校对提交，进入审核阶段
                    ('9', '审核中'),  # 审核暂存，没有提交
                    ('10', '审核提交'),  # 审核通过，进入归档阶段
                    ('11', '归档'))  # 归档完成

    name = models.CharField(max_length=50, verbose_name='项目名称')
    sn = models.CharField(max_length=50, null=True, blank=True, verbose_name='鉴定编号')
    org = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True,
                            verbose_name='鉴定机构')
    type = models.ForeignKey(AppraisalType, on_delete=models.SET_NULL, null=True,
                             verbose_name='鉴定类别')
    purpose = models.ForeignKey(AppraisalPurpose, on_delete=models.SET_NULL, null=True,
                                verbose_name='鉴定用途')
    principal = models.CharField(max_length=50, verbose_name='委托人')
    trust_detail = models.TextField(null=True, blank=True, verbose_name='委托事项')
    is_re_appraisal = models.BooleanField(verbose_name='是否重新鉴定')
    target = models.CharField(max_length=50, verbose_name='被鉴定对象')
    trust_date = models.DateField(null=True, blank=True, verbose_name='委托时间')
    created_date = models.DateField(null=True, blank=True, verbose_name='受理时间')
    creator = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name="creator", verbose_name="立项人")
    reviewer = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name="reviewer", verbose_name='立项审批人')
    stage = models.IntegerField(choices=STAGE_CHOICE, verbose_name='项目所处阶段')

    class Meta:
        verbose_name = '立项阶段信息'
        verbose_name_plural = verbose_name

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     super().save(force_insert, force_update, using, update_fields)
    #
    #     appraisal_info = AppraisalInfo()
    #     appraisal_info.basic_info = self
    #     appraisal_info.save()
    #
    #     file_phase = FilePhase()
    #     file_phase.basic_info = self
    #     file_phase.save()

    def __str__(self):
        return self.name + '立项阶段信息'


class DeviceStatus(models.Model):
    """
    设备仪器状态字典表
    """
    code = models.IntegerField(verbose_name="代码")
    name = models.CharField(max_length=20, verbose_name='状态')

    class Meta:
        verbose_name = '设备仪器状态'
        verbose_name_plural = verbose_name
        ordering = ('id',)

    def __str__(self):
        return self.name


class AvailDevicesManager(models.Manager):
    """
    自定义管理器：查询所有可申领设备。
    """

    def get_queryset(self):
        return super().get_queryset().filter(status=0)


class DeviceGroup(models.Model):
    """
    设备仪器的分类分组。
    """
    name = models.CharField(max_length=50, verbose_name="类别")

    class Meta:
        verbose_name = "设备分类"
        verbose_name_plural = verbose_name


class Devices(models.Model):
    """
    设备仪器
    """

    device_id = models.CharField(max_length=10, verbose_name='设备编号')
    name = models.CharField(max_length=50, verbose_name='设备名称')
    model = models.CharField(max_length=50, verbose_name='规格型号')
    group = models.ForeignKey(DeviceGroup, on_delete=models.DO_NOTHING, related_name="devices",
                              verbose_name="分类")
    detection_department = models.CharField(max_length=50,
                                            verbose_name='检定机构')
    detection_period = models.IntegerField(verbose_name='检定周期（月）')
    last_detection = models.DateField(verbose_name='上次检定时间')
    status = models.ForeignKey(DeviceStatus, default=1,
                               on_delete=models.DO_NOTHING, verbose_name='库存状态')

    # 指定管理器
    objects = models.Manager()
    avail_devices = AvailDevicesManager()

    class Meta:
        verbose_name = '仪器设备库'
        verbose_name_plural = verbose_name
        ordering = ('device_id',)

    def __str__(self):
        status_value = ''
        if self.status == '2':
            status_value = ' - 已出库'
        return '{} - {} ({}){}'.format(self.device_id, self.name,
                                       self.model, status_value)


class ApplyRecord(models.Model):
    """
    设备仪器出库批次记录
    """

    proposer = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING,
                                 verbose_name='申领人')
    comment = models.TextField(null=True, blank=True, verbose_name='备注')
    applied_time = models.DateTimeField(default=timezone.now, verbose_name='申领时间')
    basic_info = models.ForeignKey(BasicInfo, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name="相关项目")

    class Meta:
        verbose_name = '设备仪器申领'
        verbose_name_plural = verbose_name

    # def delete(self, using=None, keep_parents=False):
    #     # 如果申请记录被删除，则该记录对应的所有的出库设备状态恢复到在库。
    #     for item in self.applydevice_set.all():
    #         item.device.status = 1
    #         item.device.save()
    #     return super().delete(using, keep_parents)

    # def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
    #     print('ApplyRecord.save()')
    #     is_done = 1
    #     for item in self.applydevice_set.all():
    #         if item.device.status != '1':
    #             is_done = 0
    #     self.status = is_done
    #     super().save(force_insert, force_update, using, update_fields)


class ApplyRecordDetail(models.Model):
    """
    设备仪器出入库明细表
    """
    apply_record = models.ForeignKey(ApplyRecord, on_delete=models.CASCADE, verbose_name="出库批次")
    device = models.ForeignKey(Devices, on_delete=models.DO_NOTHING, verbose_name="设备")
    is_returned = models.BooleanField(default=False, verbose_name='是否归还')
    return_time = models.DateTimeField(auto_now=True, verbose_name='归还时间')

    class Meta:
        verbose_name = "设备仪器出入库明细"
        verbose_name_plural = verbose_name


# class ApplyDevice(models.Model):
#     """
#     申领设备表
#     """
#
#     # limit_choices_to的判断条件是汉字“在库”，是因为避免修改数据后，字段的id发生变化。
#     device = models.ForeignKey(Devices, on_delete=models.DO_NOTHING,
#                                # limit_choices_to={'status': '1'},
#                                verbose_name='申领设备')
#     record = models.ForeignKey(ApplyRecord, on_delete=models.CASCADE,
#                                verbose_name='申领表')
#
#     # apply_time = models.DateTimeField(auto_created=True, verbose_name='申领时间')
#     # is_return = models.BooleanField(default=False, verbose_name='是否归还')
#     # return_time = models.DateTimeField(null=True, blank=True, verbose_name='归还时间')
#
#     class Meta:
#         verbose_name = '设备'
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return '被申领设备'
#
#     def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
#         if self.record.is_return is False:
#             # 将Device表中对应记录的status改为2，代表该设备已出库，其他申领在设备列表中将看不到这个设备。
#             self.device.status = 2
#             self.device.save()
#         else:
#             self.device.status = 1
#             self.device.save()
#         super().save(force_insert, force_update, using, update_fields)
#
#     def delete(self, using=None, keep_parents=False):
#         self.device.status = 1
#         self.device.save()
#         return super().delete(using, keep_parents)


class CheckRecord(models.Model):
    """
    立项审批记录表
    """

    STATUS_CHOICE = (
        ("t", "暂存"),
        ("s", "提交"),
        ("b", "打回")
    )

    TYPE_CHOICE = (
        ("r", "立项审批"),
        ("p", "校对"),
        ("f", "最终审核")
    )

    basicInfo = models.ForeignKey(BasicInfo, on_delete=models.CASCADE, verbose_name="立项信息")
    opinion = models.TextField(verbose_name="审批意见")
    reviewer = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name="审批人")
    created_date = models.DateField(verbose_name="审批日期")
    status = models.CharField(max_length=1, choices=STATUS_CHOICE, verbose_name="操作类型")
    type = models.CharField(max_length=1, choices=TYPE_CHOICE, verbose_name="审批类型")

    class Meta:
        verbose_name = "审批记录"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}({})".format(self.basicInfo.name, str(self.status))


class AppraisalInfo(models.Model):
    """
    鉴定信息/鉴定阶段
    """

    basic_info = models.OneToOneField(BasicInfo, on_delete=models.CASCADE,
                                      related_name="appr_info",
                                      verbose_name='基础信息')

    appraisal_team = models.ManyToManyField(CustomUser, related_name='appraisal_info',
                                            verbose_name='鉴定人')

    final_reviewer = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='final_reviewer',
                                       verbose_name='复核人')
    proofreader = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name='proofreader',
                                    default=None, verbose_name='校对人')
    opinion = models.TextField(null=True, blank=True, verbose_name='主要鉴定意见')
    archivist = models.ForeignKey(CustomUser, related_name='archivist',
                                  on_delete=models.DO_NOTHING,
                                  verbose_name='立卷人')
    appraisal_address = models.CharField(max_length=50, verbose_name='鉴定地址')
    project_detail = models.TextField(null=True, blank=True, verbose_name='基本案情')
    contact = models.CharField(max_length=20, null=True, blank=True, verbose_name='联系人')
    phone = models.CharField(max_length=20, null=True, blank=True, verbose_name='联系电话')

    appraisal_date = models.DateField(verbose_name='鉴定时间')
    discuss_date = models.DateField(null=True, blank=True, verbose_name='讨论时间')

    class Meta:
        verbose_name = '鉴定阶段信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.basic_info.name + '鉴定阶段信息'


class AppraisalFile(models.Model):
    """
    鉴定材料
    """
    basic_info = models.ForeignKey(BasicInfo, on_delete=models.CASCADE,
                                   verbose_name='基本信息')
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

    def is_available(self):
        """
        判断鉴定材料是否被借阅出去，以及借阅人是谁
        :return:
        """
        record = self.records.last()
        if not record:
            return None
        else:
            is_returned = record.is_returned
            borrower = record.borrower.id
            return [is_returned, borrower]


class AppraisalFileImage(models.Model):
    """
    鉴定材料关联的图片文件
    """
    appraisal_file = models.ForeignKey(AppraisalFile, on_delete=models.CASCADE, related_name="images",
                                       verbose_name="鉴定材料")
    file = models.ImageField(upload_to='apprfiles/%Y/%m/%d', null=True, blank=True, verbose_name="上传文件")

    class Meta:
        verbose_name = "鉴定材料文件"
        verbose_name_plural = verbose_name


class AppraisalFileRecord(models.Model):
    """
    鉴定材料借阅记录
    """
    appraisal_file = models.ForeignKey(AppraisalFile, on_delete=models.CASCADE,
                                       related_name="records", verbose_name='材料')
    borrowing_time = models.DateTimeField(default=timezone.now,
                                          verbose_name='借出时间')
    return_time = models.DateTimeField(null=True, blank=True,
                                       verbose_name='归还时间')
    borrower = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING,
                                 verbose_name='借阅人')
    is_returned = models.BooleanField(null=True, blank=True, verbose_name='是否归还')
    comment = models.TextField(verbose_name='备注')

    class Meta:
        verbose_name = '材料借阅记录'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.appraisal_file.name


class LocaleFile(models.Model):
    """
    现场文件纸质文件
    通常是鉴定现场签署的签证是指委托书、协议书、现场见证取样单以及鉴定现场由法院及原被告现场确认签字的资料。
    """
    basic_info = models.ForeignKey(BasicInfo, on_delete=models.CASCADE, verbose_name='项目')
    name = models.CharField(max_length=100, verbose_name='标题')
    comment = models.TextField(null=True, blank=True, verbose_name='说明')
    created_date = models.DateField(verbose_name='接收时间')

    class Meta:
        verbose_name = '现场纸质文件'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class LocaleFileImage(models.Model):
    """
    现场纸质材料的图片文件
    """
    locale_file = models.ForeignKey(LocaleFile, on_delete=models.CASCADE,
                                    related_name="images", verbose_name="现场文件")
    file = models.ImageField(upload_to='localefiles/%Y/%m/%d', null=True, blank=True,
                             verbose_name="上传文件")

    class Meta:
        verbose_name = "现场纸质文件图片"
        verbose_name_plural = verbose_name


class AppraisalSample(models.Model):
    """
    试验检材
    """
    basic_info = models.ForeignKey(BasicInfo, on_delete=models.CASCADE,
                                   verbose_name='基本信息')
    name = models.CharField(max_length=50, verbose_name='材料名称')
    quantity = models.IntegerField(verbose_name='数量')
    received_date = models.DateField(verbose_name='接收时间')
    receiver = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING,
                                 verbose_name='接收人')

    class Meta:
        verbose_name = '试验检材'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class DeliveryState(models.Model):
    """
    送达状态
    """

    #     (1, '未送达')
    #     (2, '邮寄')
    #     (3, '专人送达')
    #     (4, '自取')

    code = models.IntegerField(verbose_name="状态码")
    name = models.CharField(max_length=50, verbose_name="送达情况")

    class Meta:
        verbose_name = "送达状态"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "状态：{}({})".format(self.code, self.name)


class FilePhase(models.Model):
    """
    档案阶段
    """
    basic_info = models.OneToOneField(BasicInfo, on_delete=models.CASCADE,
                                      verbose_name='基础信息')
    finished_date = models.DateField(null=True, blank=True, verbose_name='完成时间')
    file_date = models.DateField(null=True, blank=True, verbose_name='归档日期')
    delivery = models.ForeignKey(DeliveryState, on_delete=models.DO_NOTHING, verbose_name="送达状态")
    amount = models.IntegerField(verbose_name='份数')
    archivist = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, verbose_name="归档人")

    class Meta:
        verbose_name = '档案阶段信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.basic_info.name + '档案阶段信息'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.basic_info.stage = 3
        super().save(force_insert, force_update, using, update_fields)


class AdditionalFile(models.Model):
    """
    附加资料
    与鉴定相关的其他资料,是指报告交付以后由法院发来的问询函和其他文件，这是在鉴定后期以及报告交付后才会出现的材料。
    """
    basic_info = models.ForeignKey(BasicInfo, on_delete=models.CASCADE, verbose_name='项目')
    name = models.CharField(max_length=100, verbose_name='标题')
    comment = models.TextField(null=True, blank=True, verbose_name='说明')
    created_date = models.DateField(auto_now_add=True, verbose_name='接收日期')

    class Meta:
        verbose_name = '附加资料'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "《{}》项目的附加材料“{}”".format(self.basic_info.name, self.name)


class AddiFileImage(models.Model):
    """
    附加材料对应的图片文件
    """
    addiFile = models.ForeignKey(AdditionalFile, on_delete=models.CASCADE,
                                 related_name="images", verbose_name="附加材料")
    file = models.ImageField(upload_to='addifiles/%Y/%m/%d', verbose_name='文件')

    class Meta:
        verbose_name = "附加材料图片"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "《{}》项目的附加材料“{}”的图片{}".format(self.addiFile.basic_info.name, self.addiFile.name, self.id)


class TodoList(models.Model):
    """
    待办事项列表
    """
    # 该工作需要做什么
    TYPE_CHOICE = (
        (1, "立项"),
        (2, "初审"),
        (3, "立卷"),  # 预留，立卷人目前为抢占机制
        (4, "校对"),
        (5, "终审"),
        (6, "归档")
    )
    basic_info = models.ForeignKey(BasicInfo, on_delete=models.CASCADE, verbose_name="项目")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="责任人")
    type = models.IntegerField(choices=TYPE_CHOICE, verbose_name="事项类型")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    is_back = models.BooleanField(default=False, verbose_name="是否打回")
    finished = models.BooleanField(verbose_name="是否完成")

    class Meta:
        verbose_name = "待办事项"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "《{}》项目的“{}”工作事项".format(self.basic_info.name, self.get_type_display())
