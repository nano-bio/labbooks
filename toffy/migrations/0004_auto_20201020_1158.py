# Generated by Django 3.0.10 on 2020-10-20 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toffy', '0003_measurement_iseg_settings_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='ion_source_deflector_horizontal',
            field=models.FloatField(blank=True, null=True, verbose_name='Deflector horizontal [V]'),
        ),
        migrations.AddField(
            model_name='measurement',
            name='ion_source_deflector_vertical',
            field=models.FloatField(blank=True, null=True, verbose_name='Deflector vertical [V]'),
        ),
    ]
