# Generated by Django 3.0 on 2019-12-11 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0025_applyrecord_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='applydevice',
            name='is_return',
            field=models.BooleanField(default=False, verbose_name='是否归还'),
        ),
        migrations.AddField(
            model_name='applydevice',
            name='return_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='归还时间'),
        ),
    ]
