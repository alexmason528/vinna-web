# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-12 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0003_auto_20170710_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='businessimage',
            name='type',
            field=models.CharField(choices=[('N', 'Notification'), ('P', 'Partner')], max_length=12),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='businessimage',
            name='title',
            field=models.CharField(default='', max_length=100),
        ),
    ]