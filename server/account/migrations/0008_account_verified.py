# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-23 06:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20170721_0121'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='verified',
            field=models.BooleanField(default=0),
        ),
    ]