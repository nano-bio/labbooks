# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-07-01 16:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surftof', '0007_potentialsettings_estimated_impact_energy'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gas',
            options={'verbose_name_plural': 'gases'},
        ),
        migrations.AlterModelOptions(
            name='measurement',
            options={},
        ),
        migrations.AlterModelOptions(
            name='potentialsettings',
            options={'verbose_name_plural': 'potential settings'},
        ),
        migrations.RenameField(
            model_name='measurement',
            old_name='filament_bottom_current',
            new_name='filament_tof_bottom_current',
        ),
        migrations.RenameField(
            model_name='measurement',
            old_name='filament_bottom_potential',
            new_name='filament_tof_bottom_potential',
        ),
        migrations.RenameField(
            model_name='measurement',
            old_name='filament_current',
            new_name='filament_tof_current',
        ),
        migrations.RenameField(
            model_name='measurement',
            old_name='filament_voltage',
            new_name='filament_tof_voltage',
        ),
        migrations.RemoveField(
            model_name='potentialsettings',
            name='potential_type',
        ),
        migrations.RemoveField(
            model_name='projectile',
            name='polarity',
        ),
        migrations.AddField(
            model_name='gas',
            name='comment',
            field=models.TextField(blank=True, help_text=b'Add infos like gas bottle number, purity, reseller, ...', null=True),
        ),
        migrations.AddField(
            model_name='gas',
            name='purity',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='measurement',
            name='filament_source_current',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='measurement',
            name='filament_source_voltage',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='measurement',
            name='file_pressure_log',
            field=models.FileField(blank=True, upload_to=b'surftof/dataFilesPressure/'),
        ),
        migrations.AddField(
            model_name='measurement',
            name='rating',
            field=models.IntegerField(choices=[(1, b'1 - Science'), (2, b'2 - Interesting'), (3, b'3 - Normal'), (4, b'4 - Not interesting')], default=3),
        ),
        migrations.AddField(
            model_name='measurement',
            name='short_description',
            field=models.CharField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='potentialsettings',
            name='stepper_slit_disc_current_max',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='potentialsettings',
            name='stepper_slit_disc_current_standby',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='potentialsettings',
            name='stepper_surface_current_max',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='potentialsettings',
            name='stepper_surface_current_standby',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='potentialsettings',
            name='tdc_extraction_time',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='potentialsettings',
            name='tdc_frequency',
            field=models.FloatField(blank=True, null=True),
        ),
    ]