# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Measurement.evaluated_by'
        db.add_column(u'clustof_measurement', 'evaluated_by',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'Measurement.evaluation_file'
        db.add_column(u'clustof_measurement', 'evaluation_file',
                      self.gf('django.db.models.fields.files.FileField')(default='', max_length=100, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Measurement.evaluated_by'
        db.delete_column(u'clustof_measurement', 'evaluated_by')

        # Deleting field 'Measurement.evaluation_file'
        db.delete_column(u'clustof_measurement', 'evaluation_file')


    models = {
        u'clustof.comment': {
            'Meta': {'object_name': 'Comment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'measurement': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clustof.Measurement']"}),
            'operator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clustof.Operator']"}),
            'text': ('django.db.models.fields.TextField', [], {'max_length': '3000'}),
            'time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'clustof.currentsetting': {
            'Meta': {'object_name': 'CurrentSetting'},
            'data_filename': ('django.db.models.fields.CharField', [], {'default': "'D:\\\\Data\\\\'", 'max_length': '1500'}),
            'data_filename_time': ('django.db.models.fields.DateTimeField', [], {}),
            'deflector_1': ('django.db.models.fields.FloatField', [], {}),
            'deflector_1_time': ('django.db.models.fields.DateTimeField', [], {}),
            'deflector_2': ('django.db.models.fields.FloatField', [], {}),
            'deflector_2_time': ('django.db.models.fields.DateTimeField', [], {}),
            'electron_energy': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'electron_energy_time': ('django.db.models.fields.DateTimeField', [], {}),
            'extraction_1': ('django.db.models.fields.FloatField', [], {}),
            'extraction_1_time': ('django.db.models.fields.DateTimeField', [], {}),
            'extraction_2': ('django.db.models.fields.FloatField', [], {}),
            'extraction_2_time': ('django.db.models.fields.DateTimeField', [], {}),
            'filament_current': ('django.db.models.fields.FloatField', [], {}),
            'filament_current_time': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ion_block': ('django.db.models.fields.FloatField', [], {}),
            'ion_block_time': ('django.db.models.fields.DateTimeField', [], {}),
            'oven_1_power': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'oven_1_power_time': ('django.db.models.fields.DateTimeField', [], {}),
            'oven_1_temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'oven_1_temperature_time': ('django.db.models.fields.DateTimeField', [], {}),
            'oven_2_power': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'oven_2_power_time': ('django.db.models.fields.DateTimeField', [], {}),
            'oven_2_temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'oven_2_temperature_time': ('django.db.models.fields.DateTimeField', [], {}),
            'polarity': ('django.db.models.fields.CharField', [], {'default': "'NEG'", 'max_length': '3'}),
            'polarity_time': ('django.db.models.fields.DateTimeField', [], {}),
            'pressure_cs': ('django.db.models.fields.FloatField', [], {'default': '4e-05'}),
            'pressure_cs_time': ('django.db.models.fields.DateTimeField', [], {}),
            'pressure_ion': ('django.db.models.fields.FloatField', [], {'default': '2e-08'}),
            'pressure_ion_time': ('django.db.models.fields.DateTimeField', [], {}),
            'pressure_pu1': ('django.db.models.fields.FloatField', [], {'default': '3e-06'}),
            'pressure_pu1_time': ('django.db.models.fields.DateTimeField', [], {}),
            'pressure_pu2': ('django.db.models.fields.FloatField', [], {'default': '1e-06'}),
            'pressure_pu2_time': ('django.db.models.fields.DateTimeField', [], {}),
            'pressure_tof': ('django.db.models.fields.FloatField', [], {'default': '3e-07'}),
            'pressure_tof_time': ('django.db.models.fields.DateTimeField', [], {}),
            'pusher': ('django.db.models.fields.FloatField', [], {}),
            'pusher_time': ('django.db.models.fields.DateTimeField', [], {}),
            'temperature_he': ('django.db.models.fields.FloatField', [], {'default': '9.0'}),
            'temperature_he_time': ('django.db.models.fields.DateTimeField', [], {}),
            'tof_settings_file': ('django.db.models.fields.CharField', [], {'max_length': '1500'}),
            'tof_settings_file_time': ('django.db.models.fields.DateTimeField', [], {}),
            'trap_current': ('django.db.models.fields.FloatField', [], {}),
            'trap_current_time': ('django.db.models.fields.DateTimeField', [], {}),
            'wehnelt': ('django.db.models.fields.FloatField', [], {}),
            'wehnelt_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'clustof.journalentry': {
            'Meta': {'ordering': "['-time']", 'object_name': 'JournalEntry'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'operator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clustof.Operator']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'clustof.measurement': {
            'Meta': {'ordering': "['-time']", 'object_name': 'Measurement'},
            'data_filename': ('django.db.models.fields.CharField', [], {'default': "'D:\\\\Data\\\\'", 'max_length': '1500'}),
            'deflector_1': ('django.db.models.fields.FloatField', [], {}),
            'deflector_2': ('django.db.models.fields.FloatField', [], {}),
            'electron_energy_set': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'evaluated_by': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'evaluation_file': ('django.db.models.fields.files.FileField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'extraction_1': ('django.db.models.fields.FloatField', [], {}),
            'extraction_2': ('django.db.models.fields.FloatField', [], {}),
            'faraday_cup': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'filament_current': ('django.db.models.fields.FloatField', [], {}),
            'flagged': ('django.db.models.fields.BooleanField', [], {}),
            'housing_current': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ion_block': ('django.db.models.fields.FloatField', [], {}),
            'nozzle_diameter': ('django.db.models.fields.FloatField', [], {'default': '0.4'}),
            'operator': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['clustof.Operator']"}),
            'oven_1_power': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'oven_1_temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'oven_2_power': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'oven_2_temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'polarity': ('django.db.models.fields.CharField', [], {'default': "'NEG'", 'max_length': '3'}),
            'pressure_cs': ('django.db.models.fields.FloatField', [], {'default': '4e-05'}),
            'pressure_ion': ('django.db.models.fields.FloatField', [], {'default': '2e-08'}),
            'pressure_pu1': ('django.db.models.fields.FloatField', [], {'default': '3e-06'}),
            'pressure_pu2': ('django.db.models.fields.FloatField', [], {'default': '1e-06'}),
            'pressure_tof': ('django.db.models.fields.FloatField', [], {'default': '3e-07'}),
            'pusher': ('django.db.models.fields.FloatField', [], {}),
            'rating': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'real_electron_energy': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'scantype': ('django.db.models.fields.CharField', [], {'default': "'MS'", 'max_length': '20'}),
            'stag_pressure_he': ('django.db.models.fields.FloatField', [], {'default': '25'}),
            'substance': ('django.db.models.fields.TextField', [], {'max_length': '1500'}),
            'temperature_he': ('django.db.models.fields.FloatField', [], {'default': '9.0'}),
            'time': ('django.db.models.fields.DateTimeField', [], {}),
            'tof_settings_file': ('django.db.models.fields.CharField', [], {'max_length': '1500'}),
            'trap_current': ('django.db.models.fields.FloatField', [], {}),
            'wehnelt': ('django.db.models.fields.FloatField', [], {})
        },
        u'clustof.operator': {
            'Meta': {'object_name': 'Operator'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['clustof']