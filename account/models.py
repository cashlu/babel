from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db import models


# class Profile(models.Model):
#     GENDER_CHOICE = (
#         ('m', '男'),
#         ('f', '女'),
#     )
#     user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
#     qsid = models.CharField(max_length=20, null=False, blank=False,
#                             verbose_name='QSID')
#     gender = models.CharField(max_length=10, choices=GENDER_CHOICE, null=False,
#                               blank=False, verbose_name='性别')
#     birth_date = models.DateField(null=True, blank=True, verbose_name='出生日期')
#     graduate = models.CharField(max_length=50, null=True, blank=True,
#                                 verbose_name='毕业院校')
#     major = models.CharField(max_length=20, null=True, blank=True,
#                              verbose_name='专业')
#     graduation_date = models.DateField(null=True, blank=True,
#                                        verbose_name='毕业时间')
#     hire_date = models.DateField(null=True, blank=True, verbose_name='入职时间')
#     certificate_id = models.CharField(max_length=50, null=True, blank=True,
#                                       verbose_name='司法鉴定人资格证号')
#     is_certificated = models.BooleanField(default=False, verbose_name='是否为司法鉴定人')
#     is_viewer = models.BooleanField(default=False, verbose_name='是否为复核人')
#
#     class Meta:
#         verbose_name = '用户资料'
#         verbose_name_plural = verbose_name
#         ordering = ('-id',)
#
#     def __str__(self):
#         return self.user.username


# User默认的__str__方法返回的是用户名，如果User是别的一些Model的外键，那在admin中，下拉框
# 显示的会是用户名，而不是用户真正的全名，可以在User类的外部，重新定义一个get_fullname方法，
# 然后注入给User类的__str__方法。
def get_fullname(self):
    if self.first_name and self.last_name:
        return self.first_name + self.last_name
    else:
        return self.username


#
#
# User.add_to_class('__str__', get_fullname)


class CustomUser(AbstractUser):
    """
    自定义的用户模型，用来扩充一些字段，来替代默认的User模型。
    """

    GENDER_CHOICE = (
        ('m', '男'),
        ('f', '女'),
    )
    qsid = models.CharField(max_length=20, null=False, blank=False,
                            verbose_name='QSID')
    name = models.CharField(max_length=20, verbose_name='姓名')
    gender = models.CharField(max_length=10, choices=GENDER_CHOICE, null=False,
                              blank=False, verbose_name='性别')
    birth_date = models.DateField(null=True, blank=True, verbose_name='出生日期')
    graduate = models.CharField(max_length=50, null=True, blank=True,
                                verbose_name='毕业院校')
    major = models.CharField(max_length=20, null=True, blank=True,
                             verbose_name='专业')
    graduation_date = models.DateField(null=True, blank=True,
                                       verbose_name='毕业时间')
    hire_date = models.DateField(null=True, blank=True, verbose_name='入职时间')
    certificate_id = models.CharField(max_length=50, null=True, blank=True,
                                      verbose_name='司法鉴定人资格证号')
    is_certificated = models.BooleanField(default=False, verbose_name='是否为司法鉴定人')
    is_viewer = models.BooleanField(default=False, verbose_name='是否为复核人')

    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = verbose_name
        ordering = ('-id',)

    def __str__(self):
        return self.name

    def get_fullname(self):
        return self.name
