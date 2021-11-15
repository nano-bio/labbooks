# Generated by Django 3.2.9 on 2021-11-15 06:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nanoparticles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MeasurementData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forward_phase', models.JSONField()),
                ('forward_amplitude', models.JSONField()),
                ('forward_z_axis', models.JSONField()),
                ('backward_phase', models.JSONField()),
                ('backward_amplitude', models.JSONField()),
                ('backward_z_axis', models.JSONField()),
                ('measurement', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='nanoparticles.measurement')),
            ],
        ),
    ]
