# Generated by Django 3.0 on 2019-12-25 21:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0036_auto_20191225_2044'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='appraisalinfo',
            options={'verbose_name': '鉴定阶段信息', 'verbose_name_plural': '鉴定阶段信息'},
        ),
        migrations.AlterModelOptions(
            name='basicinfo',
            options={'verbose_name': '立项阶段信息', 'verbose_name_plural': '立项阶段信息'},
        ),
        migrations.AlterModelOptions(
            name='filephase',
            options={'verbose_name': '档案阶段信息', 'verbose_name_plural': '档案阶段信息'},
        ),
        migrations.AlterModelOptions(
            name='samplerecord',
            options={'verbose_name': '材料借阅记录', 'verbose_name_plural': '材料借阅记录'},
        ),
        migrations.AddField(
            model_name='filephase',
            name='basic_info',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='appraisal.BasicInfo', verbose_name='基础信息'),
            preserve_default=False,
        ),
    ]
