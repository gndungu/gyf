# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2021-11-17 08:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('coop', '0009_auto_20211027_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmergroupadmin',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='farmergroupadmin',
            name='farmer_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='coop.FarmerGroup'),
        ),
    ]