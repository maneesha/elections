# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-14 21:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('phlcitycouncil', '0010_auto_20160514_2155'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='candidate',
            unique_together=set([('person', 'party')]),
        ),
    ]