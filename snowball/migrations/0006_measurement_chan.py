# -*- coding: utf-8 -*-
# Generated by Django 1.10.7 on 2017-10-05 11:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snowball', '0005_measurement_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='chan',
            field=models.FloatField(default=3500.0, verbose_name=b'Channeltron Voltage'),
        ),
    ]
