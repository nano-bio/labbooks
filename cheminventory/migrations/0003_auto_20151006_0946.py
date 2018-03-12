# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cheminventory', '0002_auto_20151006_0932'),
    ]

    operations = [
        migrations.CreateModel(
            name='GasCylinderUsageRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('comment', models.CharField(max_length=100, blank=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='usagerecord',
            name='gas_cylinder',
        ),
        migrations.RemoveField(
            model_name='usagerecord',
            name='usage_location',
        ),
        migrations.RemoveField(
            model_name='gascylinder',
            name='last_used',
        ),
        migrations.RemoveField(
            model_name='gascylinder',
            name='last_user',
        ),
        migrations.RemoveField(
            model_name='gascylinder',
            name='usage_location',
        ),
        migrations.DeleteModel(
            name='UsageRecord',
        ),
        migrations.AddField(
            model_name='gascylinderusagerecord',
            name='gas_cylinder',
            field=models.ForeignKey(to='cheminventory.GasCylinder'),
        ),
        migrations.AddField(
            model_name='gascylinderusagerecord',
            name='usage_location',
            field=models.ForeignKey(to='cheminventory.UsageLocation'),
        ),
        migrations.AddField(
            model_name='gascylinderusagerecord',
            name='user',
            field=models.ForeignKey(to='cheminventory.Person'),
        ),
    ]
