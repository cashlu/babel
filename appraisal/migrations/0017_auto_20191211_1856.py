# Generated by Django 3.0 on 2019-12-11 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0016_auto_20191211_1849'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devices',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='appraisal.DeviceStatus', verbose_name='设备状态'),
        ),
    ]
