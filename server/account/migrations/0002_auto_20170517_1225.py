# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-17 12:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Language'),
        ),
    ]
