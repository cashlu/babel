# Generated by Django 3.0 on 2020-03-31 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0059_auto_20200331_1857'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appraisalfilerecord',
            name='is_returned',
            field=models.BooleanField(blank=True, null=True, verbose_name='是否归还'),
        ),
    ]
