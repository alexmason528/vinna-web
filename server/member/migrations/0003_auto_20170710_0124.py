# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-10 01:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0002_auto_20170706_1518'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='mailing_address_2',
            field=models.CharField(blank=True, default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='member',
            name='security_hash',
            field=models.CharField(blank=True, default='', max_length=32),
        ),
        migrations.AlterField(
            model_name='member',
            name='ssn_token',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]
