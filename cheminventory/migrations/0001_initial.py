# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import cheminventory.validations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chemical',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(db_index=True, max_length=100, verbose_name=b'Common Name', validators=[cheminventory.validations.validate_name])),
                ('chemical_formula', models.CharField(default=b'', validators=[cheminventory.validations.validate_chemical_formula], max_length=40, blank=True, verbose_name=b'Chemical Formula', db_index=True)),
                ('inchi', models.CharField(db_index=True, max_length=700, verbose_name=b'InChI', blank=True)),
                ('inchikey', models.CharField(db_index=True, max_length=27, verbose_name=b'InChI-Key', blank=True)),
                ('cas', models.CharField(blank=True, max_length=12, verbose_name=b'CAS-Number', validators=[cheminventory.validations.validate_CAS])),
                ('csid', models.IntegerField(null=True, verbose_name=b'CSID', blank=True)),
                ('no_chemspider_sync', models.BooleanField(default=False, verbose_name=b'Do not sync with chemspider service')),
                ('state_of_matter', models.CharField(default=b'FLUID', max_length=5, choices=[(b'FLUID', b'Fluid'), (b'GAS', b'Gas Phase'), (b'SOLID', b'Solid')])),
                ('irritant', models.BooleanField()),
                ('toxic', models.BooleanField()),
                ('explosive', models.BooleanField()),
                ('oxidizing', models.BooleanField()),
                ('flammable', models.BooleanField()),
                ('health_hazard', models.BooleanField()),
                ('corrosive', models.BooleanField()),
                ('environmentally_damaging', models.BooleanField(verbose_name=b'Environ. dam.')),
                ('h2o_reactivity', models.BooleanField()),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ChemicalInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.CharField(max_length=100, blank=True)),
                ('quantity', models.CharField(max_length=100, blank=True)),
                ('delivery_date', models.DateField(null=True, blank=True)),
                ('group', models.CharField(default=b'DENIFL', max_length=7, null=True, choices=[(b'DENIFL', b'Denifl'), (b'SCHEIER', b'Scheier')])),
                ('last_used', models.DateField(null=True, blank=True)),
                ('last_user', models.CharField(max_length=100, null=True, blank=True)),
                ('cylinder_number', models.IntegerField(max_length=3, unique=True, null=True, verbose_name=b'Number of gas cylinder in wiki', blank=True)),
                ('comments', models.TextField(max_length=1000, blank=True)),
                ('chemical', models.ForeignKey(related_name='chemical_instance', to='cheminventory.Chemical')),
            ],
        ),
        migrations.CreateModel(
            name='GasCylinder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cylinder_number', models.IntegerField(unique=True, verbose_name=b'Number of gas cylinder')),
                ('company', models.CharField(max_length=100, blank=True)),
                ('quantity', models.CharField(max_length=100, blank=True)),
                ('delivery_date', models.DateField(null=True, blank=True)),
                ('group', models.CharField(default=b'SCHEIER', max_length=7, null=True, choices=[(b'DENIFL', b'Denifl'), (b'SCHEIER', b'Scheier')])),
                ('last_used', models.DateField(null=True, blank=True)),
                ('last_user', models.CharField(max_length=100, null=True, blank=True)),
                ('comments', models.TextField(max_length=1000, blank=True)),
                ('chemical', models.ForeignKey(related_name='gas_cylinder', to='cheminventory.Chemical')),
            ],
        ),
        migrations.CreateModel(
            name='GHS_H',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=12)),
                ('text', models.CharField(max_length=400)),
            ],
            options={
                'ordering': ['number'],
                'verbose_name': 'GHS H',
                'verbose_name_plural': 'GHS H',
            },
        ),
        migrations.CreateModel(
            name='GHS_P',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number', models.CharField(max_length=12)),
                ('text', models.CharField(max_length=400)),
            ],
            options={
                'ordering': ['number'],
                'verbose_name': 'GHS P',
                'verbose_name_plural': 'GHS P',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('office_phone', models.IntegerField()),
                ('mobile', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='StorageLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('suitable_for', models.CharField(max_length=5, choices=[(b'FLUID', b'Fluid'), (b'GAS', b'Gas Phase'), (b'SOLID', b'Solid')])),
                ('toxic_or_health_hazard_necessary', models.BooleanField(default=False)),
                ('explosive_necessary', models.BooleanField(default=False)),
                ('oxidizing_necessary', models.BooleanField(default=False)),
                ('flammable_necessary', models.BooleanField(default=False)),
                ('irritant_necessary', models.BooleanField(default=False)),
                ('corrosive_necessary', models.BooleanField(default=False)),
                ('environmentally_damaging_necessary', models.BooleanField(default=False)),
                ('h2o_reactivity_necessary', models.BooleanField(default=False)),
                ('toxic_allowed', models.BooleanField(default=False)),
                ('explosive_allowed', models.BooleanField(default=False)),
                ('oxidizing_allowed', models.BooleanField(default=False)),
                ('flammable_allowed', models.BooleanField(default=False)),
                ('irritant_allowed', models.BooleanField(default=False)),
                ('corrosive_allowed', models.BooleanField(default=False)),
                ('health_hazard_allowed', models.BooleanField(default=False)),
                ('environmentally_damaging_allowed', models.BooleanField(default=False)),
                ('h2o_reactivity_allowed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='UsageLocation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('room_number', models.CharField(max_length=6)),
                ('experiment', models.TextField(max_length=1000, blank=True)),
                ('responsible_persons', models.ManyToManyField(to='cheminventory.Person')),
            ],
        ),
        migrations.CreateModel(
            name='UsageRecord',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('comment', models.CharField(max_length=100, blank=True)),
                ('gas_cylinder', models.ForeignKey(to='cheminventory.GasCylinder')),
                ('usage_location', models.ForeignKey(to='cheminventory.UsageLocation')),
            ],
        ),
        migrations.AddField(
            model_name='gascylinder',
            name='storage_location',
            field=models.ForeignKey(to='cheminventory.StorageLocation'),
        ),
        migrations.AddField(
            model_name='gascylinder',
            name='usage_location',
            field=models.ForeignKey(blank=True, to='cheminventory.UsageLocation', null=True),
        ),
        migrations.AddField(
            model_name='chemicalinstance',
            name='storage_location',
            field=models.ForeignKey(to='cheminventory.StorageLocation'),
        ),
        migrations.AddField(
            model_name='chemicalinstance',
            name='usage_location',
            field=models.ForeignKey(blank=True, to='cheminventory.UsageLocation', null=True),
        ),
        migrations.AddField(
            model_name='chemical',
            name='ghs_h',
            field=models.ManyToManyField(to='cheminventory.GHS_H', blank=True),
        ),
        migrations.AddField(
            model_name='chemical',
            name='ghs_p',
            field=models.ManyToManyField(to='cheminventory.GHS_P', blank=True),
        ),
        migrations.AlterOrderWithRespectTo(
            name='chemicalinstance',
            order_with_respect_to='chemical',
        ),
        migrations.AlterUniqueTogether(
            name='chemical',
            unique_together=set([('cas', 'state_of_matter', 'irritant', 'toxic', 'explosive', 'oxidizing', 'flammable', 'health_hazard', 'corrosive', 'environmentally_damaging', 'h2o_reactivity'), ('csid', 'state_of_matter', 'irritant', 'toxic', 'explosive', 'oxidizing', 'flammable', 'health_hazard', 'corrosive', 'environmentally_damaging', 'h2o_reactivity'), ('inchikey', 'state_of_matter', 'irritant', 'toxic', 'explosive', 'oxidizing', 'flammable', 'health_hazard', 'corrosive', 'environmentally_damaging', 'h2o_reactivity')]),
        ),
    ]
