# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-30 23:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0004_auto_20170830_2204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='total_amount',
            field=models.FloatField(default=0),
        ),
    ]
