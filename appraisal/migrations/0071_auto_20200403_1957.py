# Generated by Django 3.0 on 2020-04-03 19:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appraisal', '0070_auto_20200403_0406'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deliverystate',
            options={'verbose_name': '送达状态', 'verbose_name_plural': '送达状态'},
        ),
        migrations.RemoveField(
            model_name='additionalfile',
            name='file',
        ),
        migrations.CreateModel(
            name='AddiFileImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.ImageField(upload_to='addifiles/%Y/%m/%d', verbose_name='文件')),
                ('addiFile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='appraisal.AdditionalFile', verbose_name='附加材料')),
            ],
        ),
    ]
