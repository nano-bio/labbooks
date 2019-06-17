# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cheminventory', '0003_auto_20151006_0946'),
    ]

    operations = [
        migrations.AddField(
            model_name='gascylinder',
            name='pressure',
            field=models.FloatField(default=200),
        ),
    ]
