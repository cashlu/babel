# Generated by Django 3.0 on 2020-03-14 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_customuser_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True)),
                ('password', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=64)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.UserInfo')),
            ],
        ),
    ]
