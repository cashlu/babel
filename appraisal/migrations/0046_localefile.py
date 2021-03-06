# Generated by Django 3.0 on 2020-01-13 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0045_appraisalsample'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocaleFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='标题')),
                ('file', models.FileField(upload_to='%Y/%m/%d')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='说明')),
                ('created_date', models.DateField(auto_now_add=True, verbose_name='上传时间')),
                ('basic_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appraisal.BasicInfo', verbose_name='项目')),
            ],
            options={
                'verbose_name': '现场文件',
                'verbose_name_plural': '现场文件',
            },
        ),
    ]
