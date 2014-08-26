# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column('clustof_currentsetting', 'electron_energy', 'electron_energy_set')
        db.rename_column('clustof_currentsetting', 'electron_energy_time', 'electron_energy_set_time')
    def backwards(self, orm):
        db.rename_column('clustof_currentsetting', 'electron_energy_set', 'electron_energy')
        db.rename_column('clustof_currentsetting', 'electron_energy_set_time', 'electron_energy_time')
