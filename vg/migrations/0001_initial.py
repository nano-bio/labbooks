# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Calibration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('formula', models.CharField(max_length=100, verbose_name=b'Calibration formula for copy-pasting', blank=True)),
                ('logoutput', models.TextField(verbose_name=b'Log output of fitlib', blank=True)),
                ('p0', models.FloatField(blank=True)),
                ('p1', models.FloatField(blank=True)),
                ('p2', models.FloatField(blank=True)),
                ('comments', models.TextField(blank=True)),
                ('calibration_plot', models.FileField(upload_to=b'vg/calibrations/', blank=True)),
            ],
            options={
                'ordering': ['-time'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('comment', models.TextField()),
                ('attachment', models.FileField(default=b'', upload_to=b'vg/techjournal/', blank=True)),
            ],
            options={
                'ordering': ['-time'],
                'verbose_name_plural': 'Journal Entries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('datafile', models.FileField(max_length=400, upload_to=b'vg/%Y/%m/%d/%H/%M/%S/')),
                ('scantype', models.CharField(default=b'ES', max_length=20, choices=[(b'ES', b'Energyscan'), (b'MS', b'Massscan'), (b'MIKE', b'MIKE-Scan'), (b'CID', b'CID-Scan')])),
                ('polarity', models.CharField(default=b'NEG', max_length=3, choices=[(b'NEG', b'Negative'), (b'POS', b'Positive')])),
                ('gatetime', models.FloatField(null=True, blank=True)),
                ('electron_energy', models.FloatField(null=True, verbose_name=b'Electron Energy (for MS)', blank=True)),
                ('substance', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('channeltron', models.FloatField(default=2.3, verbose_name=b'Channeltron (kV)')),
                ('ionblock_temperature', models.PositiveIntegerField(default=160)),
                ('trap_current', models.PositiveIntegerField(default=50)),
                ('filament_current', models.FloatField()),
                ('pressure_ionblock', models.CharField(default=b'1e-6', max_length=7, verbose_name=b'Pressure Ion Block (mbar)')),
                ('pressure_analyzer', models.CharField(default=b'1e-8', max_length=7, verbose_name=b'Pressure Analyzer (mbar)')),
                ('background_pressure', models.FloatField(null=True, verbose_name=b'Background Pressure in IS (mbar)', blank=True)),
                ('ion_repeller', models.FloatField(default=5.7)),
                ('focus_coarse_1', models.PositiveIntegerField()),
                ('focus_coarse_2', models.PositiveIntegerField()),
                ('focus_fine_1', models.FloatField(default=5.0)),
                ('focus_fine_2', models.FloatField(default=5.0)),
                ('deflector_1', models.FloatField()),
                ('deflector_2', models.FloatField()),
                ('ion_energy', models.FloatField()),
                ('y_focus', models.FloatField(verbose_name=b'Y-Focus')),
                ('x_deflect', models.FloatField(verbose_name=b'Y-Deflect')),
                ('z_deflect', models.FloatField(verbose_name=b'Z-Deflect')),
                ('curve_1', models.FloatField()),
                ('rotate_1', models.FloatField()),
                ('z_deflect_1', models.FloatField(verbose_name=b'Z-Deflect 1')),
                ('z_focus_1', models.FloatField(verbose_name=b'Z-Focus 1')),
                ('curve_2', models.FloatField()),
                ('rotate_2', models.FloatField()),
                ('z_deflect_2', models.FloatField(verbose_name=b'Z-Deflect 2')),
                ('z_focus_2', models.FloatField(verbose_name=b'Z-Focus 2')),
                ('comments', models.TextField()),
            ],
            options={
                'ordering': ['-time'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
            ],
            options={
            },
            bases=(models.Model,),
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
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TurbopumpStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('current', models.FloatField()),
                ('date', models.DateField(auto_now_add=True)),
                ('pump', models.ForeignKey(to='vg.Turbopump')),
            ],
            options={
                'verbose_name_plural': 'Turbopump Status',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='measurement',
            name='operator',
            field=models.ForeignKey(to='vg.Operator'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='journalentry',
            name='operator',
            field=models.ForeignKey(to='vg.Operator'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='calibration',
            name='cal_base_file_1',
            field=models.ForeignKey(related_name='calibration_cal_base_file_1', verbose_name=b'Basefile 1 used for this cal.', blank=True, to='vg.Measurement', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='calibration',
            name='cal_base_file_2',
            field=models.ForeignKey(related_name='calibration_cal_base_file_2', verbose_name=b'Basefile 2 used for this cal.', blank=True, to='vg.Measurement', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='calibration',
            name='cal_base_file_3',
            field=models.ForeignKey(related_name='calibration_cal_base_file_3', verbose_name=b'Basefile 3 used for this cal.', blank=True, to='vg.Measurement', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='calibration',
            name='cal_base_file_4',
            field=models.ForeignKey(related_name='calibration_cal_base_file_4', verbose_name=b'Basefile 4 used for this cal.', blank=True, to='vg.Measurement', null=True),
            preserve_default=True,
        ),
    ]
