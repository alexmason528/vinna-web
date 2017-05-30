# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-30 02:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=25)),
                ('dob', models.DateField()),
                ('gender', models.CharField(choices=[('F', 'Female'), ('M', 'Male')], max_length=1)),
                ('profile_photo_url', models.CharField(blank=True, max_length=100, null=True)),
                ('last_modified_date', models.DateTimeField(auto_now=True, verbose_name='Last Modified')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Language')),
            ],
        ),
        migrations.CreateModel(
            name='AccountRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Account')),
            ],
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('description', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='accountrole',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Role'),
        ),
        migrations.AddField(
            model_name='account',
            name='roles',
            field=models.ManyToManyField(through='account.AccountRole', to='account.Role'),
        ),
        migrations.AddField(
            model_name='account',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='accountrole',
            unique_together=set([('account', 'role')]),
        ),
    ]
