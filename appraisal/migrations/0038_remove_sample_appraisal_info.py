# Generated by Django 3.0 on 2020-01-02 17:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0037_auto_20191225_2113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sample',
            name='appraisal_info',
        ),
    ]
