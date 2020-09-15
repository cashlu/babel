# Generated by Django 3.1 on 2020-09-14 22:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appraisal', '0087_remove_basicinforeviews_is_passed'),
    ]

    operations = [
        migrations.CreateModel(
            name='CheckRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opinion', models.TextField(verbose_name='审批意见')),
                ('created_date', models.DateField(verbose_name='审批日期')),
                ('status', models.IntegerField(choices=[(0, '暂存'), (1, '提交'), (2, '打回')], verbose_name='操作类型')),
                ('type', models.CharField(choices=[('r', '立项审批'), ('p', '校对'), ('f', '最终审核')], max_length=1, verbose_name='审批类型')),
                ('basicInfo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appraisal.basicinfo', verbose_name='立项信息')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='审批人')),
            ],
            options={
                'verbose_name': '立项审批记录',
                'verbose_name_plural': '立项审批记录',
            },
        ),
        migrations.DeleteModel(
            name='BasicInfoReviews',
        ),
    ]
