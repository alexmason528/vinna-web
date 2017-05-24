# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-23 16:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('business', '0001_initial'),
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('review', models.CharField(blank=True, max_length=100, null=True)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.Business')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='member.Member')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='review',
            unique_together=set([('member', 'business')]),
        ),
    ]