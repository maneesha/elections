# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-14 18:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phlcitycouncil', '0005_term'),
    ]

    operations = [
        migrations.AlterField(
            model_name='election',
            name='election_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='person',
            name='birthdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='term',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='term',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='term',
            name='start_date',
            field=models.DateField(),
        ),
    ]
