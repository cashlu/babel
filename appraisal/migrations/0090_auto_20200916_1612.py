# Generated by Django 3.1 on 2020-09-16 16:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0089_auto_20200914_2259'),
    ]

    operations = [
        migrations.RenameField(
            model_name='appraisalinfo',
            old_name='reviewer',
            new_name='final_reviewer',
        ),
    ]
