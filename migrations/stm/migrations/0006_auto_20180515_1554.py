# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-15 13:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stm', '0005_auto_20180515_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='notes',
            field=models.TextField(blank=True, max_length=1000),
        ),
        migrations.AddField(
            model_name='measurement',
            name='notes',
            field=models.TextField(blank=True, max_length=1000),
        ),
    ]
