# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-14 03:19
from __future__ import unicode_literals

from django.db import migrations, models
import server.business.models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_auto_20170710_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='picture1',
            field=models.ImageField(blank=True, null=True, upload_to=server.business.models.upload_profile_image_to),
        ),
        migrations.AddField(
            model_name='business',
            name='picture2',
            field=models.ImageField(blank=True, null=True, upload_to=server.business.models.upload_profile_image_to),
        ),
        migrations.AddField(
            model_name='business',
            name='picture3',
            field=models.ImageField(blank=True, null=True, upload_to=server.business.models.upload_profile_image_to),
        ),
        migrations.AddField(
            model_name='business',
            name='picture4',
            field=models.ImageField(blank=True, null=True, upload_to=server.business.models.upload_profile_image_to),
        ),
    ]