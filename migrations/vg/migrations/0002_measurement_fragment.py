# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-05 15:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vg', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='fragment',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
