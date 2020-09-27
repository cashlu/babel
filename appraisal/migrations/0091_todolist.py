# Generated by Django 3.1 on 2020-09-21 16:43

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appraisal', '0090_auto_20200916_1612'),
    ]

    operations = [
        migrations.CreateModel(
            name='TodoList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.IntegerField(choices=[(1, '初审'), (2, '立卷'), (3, '校对'), (4, '终审'), (5, '归档')], verbose_name='事项类型')),
                ('created_time', models.DateTimeField(default=datetime.datetime(2020, 9, 21, 16, 43, 18, 406498), verbose_name='创建时间')),
                ('finished', models.BooleanField(verbose_name='是否完成')),
                ('basic_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appraisal.basicinfo', verbose_name='项目')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='责任人')),
            ],
        ),
    ]