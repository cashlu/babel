# Generated by Django 3.0 on 2019-12-10 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0002_organization'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='supervision',
        ),
        migrations.AddField(
            model_name='organization',
            name='supervision_1',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='业务主管部门1'),
        ),
        migrations.AddField(
            model_name='organization',
            name='supervision_2',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='业务主管部门2'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='account',
            field=models.CharField(max_length=50, verbose_name='开户行账号'),
        ),
    ]
