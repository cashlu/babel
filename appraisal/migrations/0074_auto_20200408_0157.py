# Generated by Django 3.0 on 2020-04-08 01:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0073_auto_20200408_0113'),
    ]

    operations = [
        migrations.RenameField(
            model_name='devicestatus',
            old_name='status',
            new_name='name',
        ),
    ]
