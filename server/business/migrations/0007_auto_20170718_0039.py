# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-18 00:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0006_auto_20170717_1633'),
    ]

    operations = [
        migrations.AlterField(
            model_name='businessbillinginfo',
            name='address2',
            field=models.CharField(blank=True, default='', max_length=40),
        ),
    ]
