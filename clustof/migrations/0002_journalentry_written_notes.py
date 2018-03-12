# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clustof', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='journalentry',
            name='written_notes',
            field=models.ImageField(upload_to=b'clustof/techjournal/notes/', blank=True),
        ),
    ]
