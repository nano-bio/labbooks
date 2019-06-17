# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clustof', '0003_auto_20150721_1013'),
    ]

    operations = [
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
    ]
