# Generated by Django 3.1.3 on 2021-01-06 23:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0108_applyrecord_apply_purpose'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applyrecorddetail',
            name='device',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appraisal.devices', verbose_name='设备'),
        ),
    ]
