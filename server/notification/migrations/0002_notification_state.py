# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-19 21:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='state',
            field=models.BooleanField(default=0),
        ),
    ]
