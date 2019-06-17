# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-02-05 13:43
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cheminventory', '0007_chemicalinstance_item_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='GaugeType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=30)),
                ('type', models.CharField(max_length=50)),
                ('modus', models.CharField(choices=[(b'PIR', b'Pirani'), (b'FULL', b'Full Range'), (b'COLD', b'Cold Cathode')], max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='PressureGauge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=4)),
                ('gauge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labinventory.GaugeType')),
                ('usage_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cheminventory.UsageLocation')),
            ],
        ),
        migrations.CreateModel(
            name='PressureGaugeUsageRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('comment', models.CharField(blank=True, max_length=100)),
                ('gauge', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='labinventory.PressureGauge')),
                ('usage_location', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cheminventory.UsageLocation')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cheminventory.Person')),
            ],
        ),
    ]
