# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-05 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wippi', '0002_measurement_base_pressure'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='fragment',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
