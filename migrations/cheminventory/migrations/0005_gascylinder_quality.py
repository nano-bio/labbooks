# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cheminventory', '0004_gascylinder_pressure'),
    ]

    operations = [
        migrations.AddField(
            model_name='gascylinder',
            name='quality',
            field=models.FloatField(default=5.0),
        ),
    ]
