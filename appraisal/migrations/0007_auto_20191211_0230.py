# Generated by Django 3.0 on 2019-12-11 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0006_auto_20191211_0149'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applyrecord',
            name='devices_apply',
            field=models.ManyToManyField(limit_choices_to={'status': 0}, related_name='apply_records', to='appraisal.Devices', verbose_name='申领设备'),
        ),
    ]
