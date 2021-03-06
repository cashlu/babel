# Generated by Django 3.0 on 2020-04-02 04:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0062_remove_localefile_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='localefile',
            name='created_date',
            field=models.DateField(verbose_name='接收时间'),
        ),
        migrations.AlterField(
            model_name='localefileimage',
            name='locale_file',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='appraisal.LocaleFile', verbose_name='现场文件'),
        ),
    ]
