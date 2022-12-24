# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2021-08-20 00:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('partner', '0001_initial'),
        ('coop', '0003_farmergroup_contact_person_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmergroup',
            name='partner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='partner.Partner'),
        ),
    ]
