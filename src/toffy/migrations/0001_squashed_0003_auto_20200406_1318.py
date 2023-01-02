# Generated by Django 3.0.8 on 2020-07-02 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('toffy', '0001_initial'), ('toffy', '0002_rename_fields'), ('toffy', '0003_auto_20200406_1318')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('short_description', models.CharField(blank=True, max_length=500)),
                ('integration_start', models.IntegerField(blank=True, null=True, verbose_name=b'Integration start [s]')),
                ('integration_stop', models.IntegerField(blank=True, null=True, verbose_name=b'Integration stop [s]')),
                ('data_file', models.FileField(blank=True, help_text=b'Export massspecs and upload plain text files only.', upload_to=b'toffy/dataFiles/')),
                ('tof_settings_file', models.FileField(blank=True, upload_to=b'toffy/settingsFiles/', verbose_name=b'TOF settings file')),
                ('comment', models.TextField(blank=True, max_length=5000)),
                ('he_pressure', models.FloatField(blank=True, default=20, null=True, verbose_name=b'He pressure [bar]')),
                ('nozzle_temperature', models.FloatField(blank=True, null=True, verbose_name=b'Nozzle temperature [K]')),
                ('ion_block_potential', models.FloatField(blank=True, null=True, verbose_name=b'Ion block potential [V]')),
                ('electron_energy', models.FloatField(blank=True, null=True, verbose_name=b'Electron energy [eV]')),
                ('electron_current', models.FloatField(blank=True, null=True, verbose_name=b'Electron current [uA]')),
                ('bender_float_voltage', models.FloatField(blank=True, null=True, verbose_name=b'Float voltage [V]')),
                ('bender_deflect_voltage', models.FloatField(blank=True, null=True, verbose_name=b'Deflect voltage [V]')),
                ('deflector_float_z', models.FloatField(blank=True, null=True, verbose_name=b'Float Z [V]')),
                ('deflector_u_z', models.FloatField(blank=True, null=True, verbose_name=b'U Z [V]')),
                ('deflector_float_y', models.FloatField(blank=True, null=True, verbose_name=b'Float Y [V]')),
                ('deflector_u_y', models.FloatField(blank=True, null=True, verbose_name=b'U Y [V]')),
                ('deflector_front_aperture', models.FloatField(blank=True, null=True, verbose_name=b'Front aperture [V]')),
                ('oven_voltage', models.FloatField(blank=True, null=True, verbose_name=b'Voltage [V]')),
                ('oven_current', models.FloatField(blank=True, null=True, verbose_name=b'Current [I]')),
                ('oven_power', models.FloatField(blank=True, null=True, verbose_name=b'Power [W]')),
                ('oven_temperature', models.FloatField(blank=True, null=True, verbose_name=b'Temperature [C]')),
                ('evaporation_gas', models.CharField(blank=True, default=b'Helium', max_length=100, null=True, verbose_name=b'Gas')),
                ('evaporation_pressure', models.FloatField(blank=True, null=True, verbose_name=b'Pressure [mbar]')),
                ('collision_gas', models.CharField(blank=True, default=b'Argon', max_length=100, null=True, verbose_name=b'Gas')),
                ('collision_pressure', models.FloatField(blank=True, null=True, verbose_name=b'Pressure [mbar]')),
                ('collision_energy', models.FloatField(blank=True, null=True, verbose_name=b'Energy [eV]')),
                ('operator', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='toffy.Operator')),
            ],
            options={
                'ordering': ['-time'],
                'get_latest_by': 'time',
            },
        ),
    ]