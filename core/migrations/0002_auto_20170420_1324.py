# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-20 13:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='state',
            old_name='name',
            new_name='text',
        ),
    ]
