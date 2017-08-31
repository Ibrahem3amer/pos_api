# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-30 23:11
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0005_auto_20170830_2307'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='discount',
            field=models.FloatField(default=0, validators=[django.core.validators.MinValueValidator(0, 'Price cannot be negative!')]),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0, 'Price cannot be negative!')]),
        ),
        migrations.AlterField(
            model_name='item',
            name='stock_amount',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0, 'Stock is empty!')]),
        ),
        migrations.AlterField(
            model_name='receipt',
            name='paid_amount',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0, 'Money cannot be negative!')]),
        ),
    ]