# Generated by Django 3.0.8 on 2020-07-03 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toffy', '0001_squashed_0003_auto_20200406_1318'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='bender_deflect_voltage',
            field=models.FloatField(blank=True, null=True, verbose_name='Deflect voltage [V]'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='bender_float_voltage',
            field=models.FloatField(blank=True, null=True, verbose_name='Float voltage [V]'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='collision_energy',
            field=models.FloatField(blank=True, null=True, verbose_name='Energy [eV]'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='collision_gas',
            field=models.CharField(blank=True, default='Argon', max_length=100, null=True, verbose_name='Gas'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='collision_pressure',
            field=models.FloatField(blank=True, null=True, verbose_name='Pressure [mbar]'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='data_file',
            field=models.FileField(blank=True, help_text='Export massspecs and upload plain text files only.', upload_to='toffy/dataFiles/'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='deflector_float_y',
            field=models.FloatField(blank=True, null=True, verbose_name='Float Y [V]'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='deflector_float_z',
            field=models.FloatField(blank=True, null=True, verbose_name='Float Z [V]'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='deflector_front_aperture',
            field=models.FloatField(blank=True, null=True, verbose_name='Front aperture [V]'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='deflector_u_y',
            field=models.FloatField(blank=True, null=True, verbose_name='U Y [V]'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='deflector_u_z',
            field=models.FloatField(blank=True, null=True, verbose_name='U Z [V]'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='electron_current',
            field=models.FloatField(blank=True, null=True, verbose_name='Electron current [uA]'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='electron_energy',
            field=models.FloatField(blank=True, null=True, verbose_name='Electron energy [eV]'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='evaporation_gas',
            field=models.CharField(blank=True, default='Helium', max_length=100, null=True, verbose_name='Gas'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='evaporation_pressure',
            field=models.FloatField(blank=True, null=True, verbose_name='Pressure [mbar]'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='he_pressure',
            field=models.FloatField(blank=True, default=20, null=True, verbose_name='He pressure [bar]'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='integration_start',
            field=models.IntegerField(blank=True, null=True, verbose_name='Integration start [s]'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='integration_stop',
            field=models.IntegerField(blank=True, null=True, verbose_name='Integration stop [s]'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='ion_block_potential',
            field=models.FloatField(blank=True, null=True, verbose_name='Ion block potential [V]'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='nozzle_temperature',
            field=models.FloatField(blank=True, null=True, verbose_name='Nozzle temperature [K]'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='oven_current',
            field=models.FloatField(blank=True, null=True, verbose_name='Current [I]'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='oven_power',
            field=models.FloatField(blank=True, null=True, verbose_name='Power [W]'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='oven_temperature',
            field=models.FloatField(blank=True, null=True, verbose_name='Temperature [C]'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='oven_voltage',
            field=models.FloatField(blank=True, null=True, verbose_name='Voltage [V]'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='tof_settings_file',
            field=models.FileField(blank=True, upload_to='toffy/settingsFiles/', verbose_name='TOF settings file'),
        ),
    ]
