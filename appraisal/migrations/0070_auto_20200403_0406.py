# Generated by Django 3.0 on 2020-04-03 04:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0069_auto_20200403_0338'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryState',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.IntegerField(verbose_name='状态码')),
                ('name', models.CharField(max_length=50, verbose_name='送达情况')),
            ],
        ),
        migrations.AlterField(
            model_name='filephase',
            name='delivery',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='appraisal.DeliveryState', verbose_name='送达状态'),
        ),
    ]
