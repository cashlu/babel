# Generated by Django 3.0 on 2020-04-02 22:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0064_basicinfo_id_finished'),
    ]

    operations = [
        migrations.RenameField(
            model_name='basicinfo',
            old_name='id_finished',
            new_name='is_finished',
        ),
    ]