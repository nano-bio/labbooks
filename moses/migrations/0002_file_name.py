# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-03-19 13:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='name',
            field=models.CharField(default='Test', max_length=30),
            preserve_default=False,
        ),
    ]