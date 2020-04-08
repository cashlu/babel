# Generated by Django 3.0 on 2020-03-19 02:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('restfulapi', '0004_auto_20200319_0055'),
    ]

    operations = [
        migrations.AddField(
            model_name='menus',
            name='groups',
            field=models.ManyToManyField(to='auth.Group', verbose_name='分组'),
        ),
        migrations.AlterField(
            model_name='menus',
            name='level',
            field=models.IntegerField(choices=[(1, '一级菜单'), (2, '二级菜单')], default=2, verbose_name='菜单级别'),
        ),
    ]
