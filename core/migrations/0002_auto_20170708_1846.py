# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-08 18:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userlog',
            name='ip',
            field=models.CharField(max_length=40),
        ),
    ]
