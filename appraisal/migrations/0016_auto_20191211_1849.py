# Generated by Django 3.0 on 2019-12-11 18:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0015_auto_20191211_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applyrecord',
            name='apply_purpose',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='appraisal.DeviceStatus', verbose_name='申领原因'),
        ),
    ]
