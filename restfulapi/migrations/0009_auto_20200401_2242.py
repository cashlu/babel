# Generated by Django 3.0 on 2020-04-01 22:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restfulapi', '0008_auto_20200320_1809'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menus',
            options={'ordering': ['menu_id'], 'verbose_name': '菜单项', 'verbose_name_plural': '菜单项'},
        ),
    ]
