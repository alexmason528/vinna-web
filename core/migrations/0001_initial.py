# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-09 06:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_country_code', models.CharField(max_length=5)),
                ('abbrev', models.CharField(max_length=5)),
                ('text', models.CharField(max_length=50)),
                ('english_text', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Language',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=4)),
                ('text', models.CharField(max_length=50)),
                ('english_text', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abbrev', models.CharField(max_length=5)),
                ('text', models.CharField(max_length=50)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Country')),
                ('language', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Language')),
            ],
        ),
        migrations.AddField(
            model_name='country',
            name='default_language',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Language'),
        ),
    ]