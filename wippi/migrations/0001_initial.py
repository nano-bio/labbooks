# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Operator'
        db.create_table('wippi_operator', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
        ))
        db.send_create_signal('wippi', ['Operator'])

        # Adding model 'Measurement'
        db.create_table('wippi_measurement', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('operator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wippi.Operator'])),
            ('time', self.gf('django.db.models.fields.DateTimeField')()),
            ('datafile', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('scantype', self.gf('django.db.models.fields.CharField')(default='ES', max_length=20)),
            ('gatetime', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('polarity', self.gf('django.db.models.fields.CharField')(default='NEG', max_length=3)),
            ('electron_energy', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('ion_energy', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('substance', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('channeltron_1', self.gf('django.db.models.fields.FloatField')(default=5.8, null=True, blank=True)),
            ('channeltron_2', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('oven_temperature', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('chamber_temperature', self.gf('django.db.models.fields.PositiveIntegerField')(default=90, null=True, blank=True)),
            ('faraday_current', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('filament_current', self.gf('django.db.models.fields.FloatField')(default=2.36)),
            ('emission', self.gf('django.db.models.fields.PositiveIntegerField')(null=True, blank=True)),
            ('energy_resolution', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mass_resolution', self.gf('django.db.models.fields.FloatField')(default=25, null=True, blank=True)),
            ('pressure_monochromator', self.gf('django.db.models.fields.CharField')(default='2e-6', max_length=7)),
            ('pressure_pickup', self.gf('django.db.models.fields.CharField')(max_length=7, blank=True)),
            ('pressure_cs', self.gf('django.db.models.fields.CharField')(max_length=7, blank=True)),
            ('background_pressure', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('anode', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('def_a', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('def_i', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('optics_inside', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('optics_outside', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('coil_voltage_xy', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('coil_voltage_xz', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('coil_voltage_yz', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('coil_current_xy', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('coil_current_xz', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('coil_current_yz', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('lens_1a', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_1b', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_1c', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_A1', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_L2', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_L3', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_2a', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_2b', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_2c', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_L4', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_L5', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_D1', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_D2', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_Ua', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_Ui', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('uhk_mitte', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_3a', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_3b', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_3c', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_A2', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_L6', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_L7', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_4a', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_4b', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_4c', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_L8', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('uex_mitte', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('lens_A3', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('lens_L10', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('lens_SK1', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('lens_SK2', self.gf('django.db.models.fields.FloatField')(default=0, null=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('wippi', ['Measurement'])

        # Adding model 'Calibration'
        db.create_table('wippi_calibration', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('cal_base_file_1', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='calibration_cal_base_file_1', null=True, to=orm['wippi.Measurement'])),
            ('cal_base_file_2', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='calibration_cal_base_file_2', null=True, to=orm['wippi.Measurement'])),
            ('cal_base_file_3', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='calibration_cal_base_file_3', null=True, to=orm['wippi.Measurement'])),
            ('cal_base_file_4', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='calibration_cal_base_file_4', null=True, to=orm['wippi.Measurement'])),
            ('formula', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('logoutput', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('p0', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('p1', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('p2', self.gf('django.db.models.fields.FloatField')(blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('calibration_plot', self.gf('django.db.models.fields.files.FileField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('wippi', ['Calibration'])

        # Adding model 'JournalEntry'
        db.create_table('wippi_journalentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('operator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['wippi.Operator'])),
            ('comment', self.gf('django.db.models.fields.TextField')()),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(default='', max_length=100, blank=True)),
        ))
        db.send_create_signal('wippi', ['JournalEntry'])


    def backwards(self, orm):
        # Deleting model 'Operator'
        db.delete_table('wippi_operator')

        # Deleting model 'Measurement'
        db.delete_table('wippi_measurement')

        # Deleting model 'Calibration'
        db.delete_table('wippi_calibration')

        # Deleting model 'JournalEntry'
        db.delete_table('wippi_journalentry')


    models = {
        'wippi.calibration': {
            'Meta': {'ordering': "['-time']", 'object_name': 'Calibration'},
            'cal_base_file_1': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'calibration_cal_base_file_1'", 'null': 'True', 'to': "orm['wippi.Measurement']"}),
            'cal_base_file_2': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'calibration_cal_base_file_2'", 'null': 'True', 'to': "orm['wippi.Measurement']"}),
            'cal_base_file_3': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'calibration_cal_base_file_3'", 'null': 'True', 'to': "orm['wippi.Measurement']"}),
            'cal_base_file_4': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'calibration_cal_base_file_4'", 'null': 'True', 'to': "orm['wippi.Measurement']"}),
            'calibration_plot': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'formula': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logoutput': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'p0': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'p1': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'p2': ('django.db.models.fields.FloatField', [], {'blank': 'True'}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'wippi.journalentry': {
            'Meta': {'ordering': "['-time']", 'object_name': 'JournalEntry'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'operator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wippi.Operator']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'wippi.measurement': {
            'Meta': {'ordering': "['-time']", 'object_name': 'Measurement'},
            'anode': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'background_pressure': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'chamber_temperature': ('django.db.models.fields.PositiveIntegerField', [], {'default': '90', 'null': 'True', 'blank': 'True'}),
            'channeltron_1': ('django.db.models.fields.FloatField', [], {'default': '5.8', 'null': 'True', 'blank': 'True'}),
            'channeltron_2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'coil_current_xy': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'coil_current_xz': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'coil_current_yz': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'coil_voltage_xy': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'coil_voltage_xz': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'coil_voltage_yz': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'datafile': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'def_a': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'def_i': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'electron_energy': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'emission': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'energy_resolution': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'faraday_current': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'filament_current': ('django.db.models.fields.FloatField', [], {'default': '2.36'}),
            'gatetime': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ion_energy': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_1a': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_1b': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_1c': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_2a': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_2b': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_2c': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_3a': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_3b': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_3c': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_4a': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_4b': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_4c': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_A1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_A2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_A3': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'lens_D1': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_D2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_L10': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'lens_L2': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_L3': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_L4': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_L5': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_L6': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_L7': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_L8': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_SK1': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'lens_SK2': ('django.db.models.fields.FloatField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'lens_Ua': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lens_Ui': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mass_resolution': ('django.db.models.fields.FloatField', [], {'default': '25', 'null': 'True', 'blank': 'True'}),
            'operator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['wippi.Operator']"}),
            'optics_inside': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'optics_outside': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'oven_temperature': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'polarity': ('django.db.models.fields.CharField', [], {'default': "'NEG'", 'max_length': '3'}),
            'pressure_cs': ('django.db.models.fields.CharField', [], {'max_length': '7', 'blank': 'True'}),
            'pressure_monochromator': ('django.db.models.fields.CharField', [], {'default': "'2e-6'", 'max_length': '7'}),
            'pressure_pickup': ('django.db.models.fields.CharField', [], {'max_length': '7', 'blank': 'True'}),
            'scantype': ('django.db.models.fields.CharField', [], {'default': "'ES'", 'max_length': '20'}),
            'substance': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'uex_mitte': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'uhk_mitte': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        'wippi.operator': {
            'Meta': {'object_name': 'Operator'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['wippi']