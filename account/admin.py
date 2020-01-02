from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser


# class ProfileInlineAdmin(admin.StackedInline):
# #     model = Profile
# #     can_delete = False
# #     verbose_name_plural = 'profile'
# #
# #
# # class UserAdmin(BaseUserAdmin):
# #     inlines = (ProfileInlineAdmin,)
# #
# #
# # admin.site.unregister(User)
# # admin.site.register(User, UserAdmin)


# 注册自定义的User模型
# admin.site.register(CustomUser, UserAdmin)


# @admin.register(CustomUser)
# class CustomUserAdmin(UserAdmin):
# 方法可行
# list_display = ('username', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined')
# fieldsets = (
#     (None, {'fields': ('username', 'password', 'first_name', 'last_name', 'email',)}),
#     (gettext_lazy('User Information'), {'fields': ('qsid', 'gender', 'birth_date',
#                                                    'graduate', 'major', 'graduation_date',
#                                                    'hire_date', 'certificate_id',
#                                                    'is_certificated', 'is_viewer')}),
#     (gettext_lazy('Permissions'), {'fields': ('is_superuser', 'is_staff', 'is_active',
#                                               'groups', 'user_permissions')}),
#     (gettext_lazy('Important dates'), {'fields': ('last_login', 'date_joined')}),
# )

# 下面这种方法可行
# list_display = ('qsid', 'username', 'name', 'email',)
# fieldsets = UserAdmin.fieldsets + ((gettext_lazy('其他信息'),
#                                     {'fields': ('qsid', 'name', 'gender', 'birth_date',
#                                                 'graduate', 'major', 'graduation_date',
#                                                 'hire_date', 'certificate_id',
#                                                 'is_certificated', 'is_viewer')}),)


# 这个方法不可行，需要指定fieldsets的元素。
# fieldsets = ()
# add_fieldsets = (
#     (None, {
#         'classes': ('wide',),
#         'fields': ('qsid', 'gender', 'birth_date', 'graduate', 'major', 'graduation_date',
#                    'hire_date', 'certificate_id', 'is_certificated', 'is_viewer')
#     }),
# )


class MyUserCreationForm(UserCreationForm):
    """自定义用户创建的表单"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 指定email和name为必填项
        # email字段在Django的源代码中已经定义了，这里重写的目的是为了让该字段成为必填项。
        self.fields['email'].required = True
        self.fields['name'].required = True


class MyUserChangeForm(UserChangeForm):
    """自定义用户修改的表单"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        self.fields['name'].required = True


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display_links = ('qsid', 'username', 'name',)

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.list_display = ('qsid', 'username', 'name', 'email', 'is_active', 'is_staff',
                             'is_superuser',)
        self.search_fields = ('username', 'name', 'email',)
        # 修改用户表单
        self.form = MyUserChangeForm
        # 添加用户表单
        self.add_form = MyUserCreationForm

        self.fieldsets = (
            (None, {'fields': ('username', 'password',)}),
            ('用户信息', {'fields': ('name', 'qsid', 'email', 'gender', 'birth_date',)}),
            ('学历资质信息', {'fields': (
                'graduate', 'major', 'graduation_date', 'hire_date', 'is_certificated',
                'certificate_id', 'is_viewer')}),
            ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
            ('注册登录记录', {'fields': ('last_login', 'date_joined')}),
        )
        self.add_fieldsets = (
            (None, {'classes': ('wide',),
                    'fields': ('username', 'name', 'password1', 'password2', 'email', 'is_active',
                               'is_staff', 'is_superuser', 'groups'), }),
        )

    # def changelist_view(self, request, extra_context=None):
    #     if not request.user.is_superuser:
    #         self.fieldsets = (
    #             (None, {'fields': ('username', 'password',)}),
    #             ('用户信息', {'fields': ('name', 'qsid', 'email', 'gender', 'birth_date',)}),
    #             ('学历资质信息', {'fields': (
    #                 'graduate', 'major', 'graduation_date', 'hire_date', 'is_certificated',
    #                 'certificate_id', 'is_viewer')}),
    #             # ('权限', {'fields': ('is_active', 'is_staff', 'groups',)}),
    #             ('注册登录记录', {'fields': ('last_login', 'date_joined',)}),
    #
    #         )
    #
    #         self.add_fieldsets = (
    #             (None, {'classes': ('wide',),
    #                     'fields': ('username', 'name', 'password1', 'password2', 'email',
    #                                'is_active', 'is_staff', 'groups',), }),
    #         )
    #     else:
    #         self.fieldsets = (
    #             (None, {'fields': ('username', 'password',)}),
    #             ('用户信息', {'fields': ('name', 'qsid', 'email', 'gender', 'birth_date',)}),
    #             ('学历资质信息', {'fields': (
    #                 'graduate', 'major', 'graduation_date', 'hire_date', 'is_certificated',
    #                 'certificate_id', 'is_viewer')}),
    #             ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
    #             ('注册登录记录', {'fields': ('last_login', 'date_joined')}),
    #         )
    #         self.add_fieldsets = (
    #             (None, {'classes': ('wide',),
    #                     'fields': ('username', 'name', 'password1', 'password2', 'email', 'is_active',
    #                                'is_staff', 'is_superuser', 'groups'), }),
    #         )
    #     return super().changelist_view(request, extra_context)
