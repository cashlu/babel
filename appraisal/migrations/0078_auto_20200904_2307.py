# Generated by Django 3.1 on 2020-09-04 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0077_auto_20200903_1359'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basicinfo',
            name='stage',
            field=models.IntegerField(choices=[('1', '在库'), ('2', '出库')], max_length=1, verbose_name='项目所处阶段'),
        ),
    ]
