# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-16 08:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0004_auto_20170716_0712'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='rating',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
