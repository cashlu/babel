# Generated by Django 3.1 on 2020-09-23 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0095_auto_20200923_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkrecord',
            name='status',
            field=models.IntegerField(choices=[('t', '暂存'), ('s', '提交'), ('b', '打回')], verbose_name='操作类型'),
        ),
    ]