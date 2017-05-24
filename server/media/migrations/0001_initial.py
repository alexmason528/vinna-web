# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-23 16:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusinessImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=100)),
                ('s3_url', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500, null=True)),
                ('business', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='business.Business')),
            ],
        ),
        migrations.CreateModel(
            name='BusinessVideo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=100)),
                ('unique_code', models.CharField(max_length=100, unique=True)),
                ('platform', models.CharField(choices=[('Y', 'Youtube'), ('V', 'Vimeo')], max_length=1)),
                ('business', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='business.Business')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hash', models.CharField(max_length=100)),
                ('s3_url', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.CharField(max_length=100)),
                ('unique_code', models.CharField(max_length=100, unique=True)),
                ('platform', models.CharField(choices=[('Y', 'Youtube'), ('V', 'Vimeo')], max_length=1)),
            ],
        ),
    ]
