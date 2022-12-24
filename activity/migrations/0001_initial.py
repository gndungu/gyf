# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2021-08-19 22:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExternalTrainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'external_trainer',
            },
        ),
        migrations.CreateModel(
            name='ThematicArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thematic_area', models.CharField(max_length=150)),
                ('description', models.TextField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'thematic_area',
            },
        ),
        migrations.CreateModel(
            name='TrainingAttendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training_reference', models.CharField(blank=True, max_length=256, null=True)),
                ('gps_location', models.CharField(blank=True, max_length=256, null=True)),
                ('training_start', models.DateTimeField()),
                ('training_end', models.DateTimeField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'training_attendance',
            },
        ),
        migrations.CreateModel(
            name='TrainingModule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=250)),
                ('descriprion', models.TextField(blank=True, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'training_module',
            },
        ),
        migrations.CreateModel(
            name='TrainingSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('training_reference', models.CharField(blank=True, max_length=256, null=True)),
                ('is_external', models.BooleanField(default=False)),
                ('topic', models.CharField(blank=True, max_length=256, null=True)),
                ('descriprion', models.TextField(blank=True, null=True)),
                ('gps_location', models.CharField(blank=True, max_length=256, null=True)),
                ('training_start', models.DateTimeField()),
                ('training_end', models.DateTimeField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'training_session',
            },
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('visit_date', models.DateField()),
                ('reason', models.CharField(max_length=160)),
                ('description', models.TextField(blank=True, null=True)),
                ('gps_coodinates', models.CharField(blank=True, max_length=256, null=True)),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'partner_visit',
            },
        ),
    ]
