# Generated by Django 3.0 on 2020-01-07 17:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appraisal', '0042_auto_20200107_1625'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appraisalinfo',
            name='created_date',
        ),
        migrations.RemoveField(
            model_name='appraisalinfo',
            name='trust_date',
        ),
        migrations.AddField(
            model_name='basicinfo',
            name='created_date',
            field=models.DateField(blank=True, null=True, verbose_name='受理时间'),
        ),
        migrations.AddField(
            model_name='basicinfo',
            name='trust_date',
            field=models.DateField(blank=True, null=True, verbose_name='委托时间'),
        ),
        migrations.AlterField(
            model_name='appraisalinfo',
            name='appraisal_date',
            field=models.DateField(verbose_name='鉴定时间'),
        ),
        migrations.AlterField(
            model_name='appraisalinfo',
            name='archivist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='archivist', to=settings.AUTH_USER_MODEL, verbose_name='立卷人'),
        ),
        migrations.AlterField(
            model_name='appraisalinfo',
            name='reviewer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='reviewer', to=settings.AUTH_USER_MODEL, verbose_name='复核人'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='filephase',
            name='amount',
            field=models.IntegerField(verbose_name='份数'),
        ),
        migrations.AlterField(
            model_name='filephase',
            name='delivery',
            field=models.IntegerField(choices=[(0, '未送达'), (1, '邮寄'), (2, '专人送达'), (3, '自取')], default=0, verbose_name='送达方式'),
        ),
    ]
