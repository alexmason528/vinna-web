# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-10 10:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='description',
            field=models.CharField(max_length=1000),
            preserve_default=False,
        ),
    ]
