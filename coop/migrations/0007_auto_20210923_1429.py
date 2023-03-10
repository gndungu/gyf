# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2021-09-23 11:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conf', '0001_initial'),
        ('coop', '0006_auto_20210923_1427'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmergroup',
            name='county',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.County'),
        ),
        migrations.AddField(
            model_name='farmergroup',
            name='parish',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.Parish'),
        ),
        migrations.AddField(
            model_name='farmergroup',
            name='village',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
