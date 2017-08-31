# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-31 13:21
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0007_auto_20170831_1024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='stock_amount',
            field=models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0, 'Stock is empty!')]),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='paid_amount',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0, 'Money cannot be negative!')]),
        ),
    ]