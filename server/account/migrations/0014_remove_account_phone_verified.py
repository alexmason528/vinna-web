# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-09-12 15:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_auto_20170822_2312'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='phone_verified',
        ),
    ]
