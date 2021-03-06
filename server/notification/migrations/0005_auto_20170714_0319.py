# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-14 03:19
from __future__ import unicode_literals

from django.db import migrations, models
import server.notification.models


class Migration(migrations.Migration):

    dependencies = [
        ('notification', '0004_auto_20170712_1635'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='message',
        ),
        migrations.AddField(
            model_name='notification',
            name='description',
            field=models.CharField(max_length=140),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='picture',
            field=models.ImageField(upload_to=server.notification.models.upload_profile_image_to),
            preserve_default=False,
        ),
    ]
