# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-28 17:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phlcitycouncil', '0018_auto_20161121_0152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='term',
            name='departed',
            field=models.CharField(choices=[('Incumbent', 'Incumbent'), ('Defeated', 'Defeated'), ('Retired', 'Retired'), ('Resigned', 'Resigned'), ('Scandal', 'Scandal'), ('Died', 'Died')], max_length=25),
        ),
        migrations.AlterField(
            model_name='vote',
            name='ballot_type',
            field=models.CharField(blank=True, choices=[('A', 'Absentee'), ('P', 'Provisional'), ('M', 'Machine')], max_length=50, null=True),
        ),
    ]
