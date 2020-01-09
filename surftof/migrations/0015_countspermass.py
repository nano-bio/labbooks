# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-11-12 13:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('surftof', '0014_auto_20191031_0820'),
    ]

    operations = [
        migrations.CreateModel(
            name='CountsPerMass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_edit', models.DateTimeField(auto_now=True)),
                ('mass', models.FloatField(help_text=b'Use only the integer masses here, except "half masses" (28.5m/z)')),
                ('counts', models.FloatField(verbose_name=b'Normalized Counts')),
                ('counts_err', models.FloatField()),
                ('surface_impact_energy', models.FloatField(blank=True, null=True)),
                ('surface_temperature', models.FloatField(blank=True, null=True)),
                ('surface_current', models.FloatField(blank=True, null=True)),
                ('pressure_is', models.FloatField(blank=True, null=True)),
                ('pressure_surf', models.FloatField(blank=True, null=True)),
                ('pressure_tof', models.FloatField(blank=True, null=True)),
                ('molecule', models.CharField(blank=True, help_text=b'E.g. Be2D3. Only use this field, if you are sure, that the counts are not a combination of different molecules!', max_length=100, verbose_name=b'Molecular formula')),
                ('comment', models.TextField(blank=True, max_length=500)),
                ('measurement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='surftof.Measurement')),
            ],
        ),
    ]