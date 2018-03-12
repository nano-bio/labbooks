# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clustof', '0002_journalentry_written_notes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='journalentry',
            options={'ordering': ['-time'], 'verbose_name_plural': 'Journal Entries'},
        ),
    ]
