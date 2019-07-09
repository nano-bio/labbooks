# -*- coding: utf-8 -*-
# Generated by Django 1.9.9 on 2016-09-13 07:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clustof', '0007_auto_20160718_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='marked',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='nozzle_diameter',
            field=models.FloatField(default=5),
        ),
    ]