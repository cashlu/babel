# Generated by Django 3.0 on 2020-03-19 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restfulapi', '0005_auto_20200319_0231'),
    ]

    operations = [
        migrations.AddField(
            model_name='menus',
            name='url',
            field=models.CharField(max_length=50, null=True, verbose_name='url'),
        ),
    ]