# Generated by Django 3.1 on 2020-09-27 23:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0101_auto_20200927_2342'),
    ]

    operations = [
        migrations.AddField(
            model_name='devices',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='appraisal.devicegroup', verbose_name='分类'),
        ),
    ]
