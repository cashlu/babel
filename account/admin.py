from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy

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


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
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
    fieldsets = UserAdmin.fieldsets + ((gettext_lazy('其他信息'),
                                        {'fields': ('qsid', 'gender', 'birth_date',
                                                    'graduate', 'major', 'graduation_date',
                                                    'hire_date', 'certificate_id',
                                                    'is_certificated', 'is_viewer')}),)



