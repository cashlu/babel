# Generated by Django 3.0 on 2019-12-11 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0014_auto_20191211_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='applyrecord',
            name='apply_purpose',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='appraisal.DeviceStatus', verbose_name='申领原因'),
        ),
        migrations.AddField(
            model_name='devices',
            name='status',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to='appraisal.DeviceStatus', verbose_name='设备状态'),
        ),
    ]
