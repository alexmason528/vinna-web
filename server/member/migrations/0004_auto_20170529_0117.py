# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-29 01:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0003_auto_20170528_1402'),
    ]

    operations = [
        migrations.AlterField(
            model_name='memberpaymentinfo',
            name='type',
            field=models.CharField(default='bank', max_length=10),
        ),
    ]
