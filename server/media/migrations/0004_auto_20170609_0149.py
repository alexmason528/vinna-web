# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-09 01:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0003_businessimage_created_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='businessimage',
            name='created_date',
        ),
        migrations.AlterField(
            model_name='businessimage',
            name='business',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='business.Business'),
        ),
    ]