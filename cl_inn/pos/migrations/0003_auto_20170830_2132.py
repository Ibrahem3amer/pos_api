# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-08-30 21:32
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pos', '0002_item_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='cashier',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[\\u0621-\\u064Aa-zA-Z][\\u0621-\\u064Aa-zA-Z0-9]*([ ]?[\\u0621-\\u064Aa-zA-Z0-9]+)+$', 'Name cannot start with number, should consist of characters.')]),
        ),
        migrations.AlterField(
            model_name='shop',
            name='name',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[\\u0621-\\u064Aa-zA-Z][\\u0621-\\u064Aa-zA-Z0-9]*([ ]?[\\u0621-\\u064Aa-zA-Z0-9]+)+$', 'Name cannot start with number, should consist of characters.')]),
        ),
    ]
