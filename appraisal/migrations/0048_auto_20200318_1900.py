# Generated by Django 3.0 on 2020-03-18 19:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0047_auto_20200113_2300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appraisalinfo',
            name='basic_info',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='appraisal.BasicInfo', verbose_name='基础信息'),
        ),
    ]