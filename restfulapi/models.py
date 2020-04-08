from django.db import models
from django.contrib.auth.models import Group


class Menus(models.Model):
    """
    前端页面aside显示的菜单项。
    """
    LEVEL_CHOICE = (
        (1, "一级菜单"),
        (2, "二级菜单"),
    )
    menu_id = models.IntegerField(verbose_name="菜单ID")
    title = models.CharField(max_length=10, verbose_name="菜单标题")
    url = models.CharField(max_length=50, null=True, blank=True, verbose_name="url")
    level = models.IntegerField(choices=LEVEL_CHOICE, default=2, verbose_name="菜单级别")
    parent = models.ForeignKey("self", max_length=10, null=True, blank=True,
                               on_delete=models.CASCADE, related_name="subMenu",
                               verbose_name="父节点")
    groups = models.ManyToManyField(to=Group, blank=True, verbose_name="分组", related_name="group_menus")

    class Meta:
        verbose_name = "菜单项"
        verbose_name_plural = verbose_name
        ordering = ["menu_id"]

    def __str__(self):
        return "{} - {}".format(self.menu_id, self.title)
