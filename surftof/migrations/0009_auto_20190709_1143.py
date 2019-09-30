# -*- coding: utf-8 -*-
# Generated by Django 1.11.22 on 2019-07-09 09:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surftof', '0008_auto_20190701_1824'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='measurement',
            name='pressure_ion_source_line',
        ),
        migrations.AlterField(
            model_name='measurement',
            name='file_tof',
            field=models.FileField(blank=True, help_text=b'zip all tof files', upload_to=b'surftof/dataFilesTof/'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='type_file_others',
            field=models.CharField(blank=True, help_text=b'If you use "file others", specify, what kind of file will be found in \'file others\'', max_length=100),
        ),
    ]