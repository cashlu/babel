# Generated by Django 3.1.3 on 2020-12-08 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0105_auto_20200928_0426'),
    ]

    operations = [
        migrations.AlterField(
            model_name='devices',
            name='device_id',
            field=models.CharField(max_length=10, unique=True, verbose_name='设备编号'),
        ),
    ]