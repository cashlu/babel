# Generated by Django 3.1 on 2020-09-23 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0096_auto_20200923_1104'),
    ]

    operations = [
        migrations.AddField(
            model_name='todolist',
            name='is_Back',
            field=models.BooleanField(default=False, verbose_name='是否打回'),
        ),
    ]
