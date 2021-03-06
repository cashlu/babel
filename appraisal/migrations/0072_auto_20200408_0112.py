# Generated by Django 3.0 on 2020-04-08 01:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0071_auto_20200403_1957'),
    ]

    operations = [
        migrations.RenameField(
            model_name='applyrecord',
            old_name='created_time',
            new_name='applied_time',
        ),
        migrations.RenameField(
            model_name='applyrecord',
            old_name='is_return',
            new_name='is_returned',
        ),
        migrations.RemoveField(
            model_name='applyrecord',
            name='status',
        ),
        migrations.RemoveField(
            model_name='devices',
            name='next_detection',
        ),
        migrations.AddField(
            model_name='applyrecord',
            name='device',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='records', to='appraisal.Devices', verbose_name='设备'),
        ),
        migrations.AddField(
            model_name='devicestatus',
            name='code',
            field=models.IntegerField(null=True, verbose_name='代码'),
        ),
        migrations.AlterField(
            model_name='additionalfile',
            name='created_date',
            field=models.DateField(auto_now_add=True, verbose_name='接收日期'),
        ),
        migrations.AlterField(
            model_name='devices',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='appraisal.DeviceStatus', verbose_name='库存状态'),
        ),
        migrations.DeleteModel(
            name='ApplyDevice',
        ),
    ]
