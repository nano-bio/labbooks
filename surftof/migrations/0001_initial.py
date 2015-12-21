# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('comment', models.TextField()),
                ('attachment', models.FileField(default=b'', upload_to=b'clustof/techjournal/', blank=True)),
                ('written_notes', models.ImageField(upload_to=b'clustof/techjournal/notes/', blank=True)),
            ],
            options={
                'ordering': ['-time'],
                'verbose_name_plural': 'Journal Entries',
            },
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('data_filename', models.CharField(default=b'D:\\Data\\', max_length=1500, verbose_name=b'Filename')),
                ('pressure_is', models.FloatField(default=4e-05, verbose_name=b'Pressure IS')),
                ('pressure_surface', models.FloatField(default=3e-06, verbose_name=b'Pressure Surface')),
                ('pressure_cube', models.FloatField(default=1e-06, verbose_name=b'Pressure Cube')),
                ('pressure_tof', models.FloatField(default=3e-07, verbose_name=b'Pressure TOF')),
                ('u_surf', models.FloatField(null=True, verbose_name=b'Surface Potential', blank=True)),
                ('u_is', models.FloatField(null=True, verbose_name=b'IS/Quad Potential', blank=True)),
                ('surface_current', models.FloatField(null=True, blank=True)),
                ('surface_temperature', models.FloatField(null=True, blank=True)),
                ('heating_current', models.FloatField(null=True, blank=True)),
                ('surface_material', models.TextField(max_length=1500)),
                ('projectile', models.TextField(max_length=1500)),
                ('polarity', models.CharField(default=b'NEG', max_length=3, choices=[(b'NEG', b'Negative'), (b'POS', b'Positive')])),
                ('evaluated_by', models.CharField(max_length=20, blank=True)),
                ('evaluation_file', models.FileField(default=b'', upload_to=b'surftof/evaluations/', blank=True)),
            ],
            options={
                'ordering': ['-time'],
                'get_latest_by': 'time',
            },
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Turbopump',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('type', models.CharField(max_length=100, blank=True)),
                ('purchase_date', models.DateField(null=True, blank=True)),
                ('service_date', models.DateField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TurbopumpStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current', models.FloatField()),
                ('date', models.DateField(auto_now_add=True)),
                ('pump', models.ForeignKey(to='surftof.Turbopump')),
            ],
            options={
                'verbose_name_plural': 'Turbopump Status',
            },
        ),
        migrations.CreateModel(
            name='VacuumStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.IntegerField()),
                ('g1', models.FloatField(null=True, blank=True)),
                ('g2', models.FloatField(null=True, blank=True)),
                ('g3', models.FloatField(null=True, blank=True)),
                ('g4', models.FloatField(null=True, blank=True)),
                ('g5', models.FloatField(null=True, blank=True)),
                ('g6', models.FloatField(null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Vacuum Status',
            },
        ),
        migrations.AddField(
            model_name='measurement',
            name='operator',
            field=models.ForeignKey(to='surftof.Operator'),
        ),
        migrations.AddField(
            model_name='journalentry',
            name='operator',
            field=models.ForeignKey(to='surftof.Operator'),
        ),
    ]
