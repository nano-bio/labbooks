# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-28 13:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snowball', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='journalentry',
            options={'ordering': ['time'], 'verbose_name_plural': 'Journal Entries'},
        ),
    ]
