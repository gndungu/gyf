# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2022-05-11 16:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conf', '0002_region'),
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplier',
            name='county',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.County'),
        ),
        migrations.AddField(
            model_name='supplier',
            name='district',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.District'),
        ),
        migrations.AddField(
            model_name='supplier',
            name='parish',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.Parish'),
        ),
        migrations.AddField(
            model_name='supplier',
            name='sub_county',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='conf.SubCounty'),
        ),
    ]