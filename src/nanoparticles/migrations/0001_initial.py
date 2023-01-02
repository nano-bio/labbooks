# Generated by Django 3.2.9 on 2021-11-23 16:54

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('comment', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('device', models.CharField(choices=[('AFM', 'AFM'), ('STM', 'STM')], max_length=10)),
                ('rating', models.IntegerField(choices=[(5, '5 - Science'), (4, '4 - Interesting'), (3, '3 - Normal'), (2, '2 - Not interesting'), (1, '1 - Trash')], default=3)),
                ('tip', models.CharField(blank=True, max_length=500)),
                ('thickness', models.FloatField(blank=True, null=True, verbose_name='Thickness  (nm)')),
                ('sputter_time', models.FloatField(blank=True, null=True, verbose_name='Sputter Time (min)')),
                ('sputter_method', models.CharField(blank=True, choices=[('magnetronTi', 'Magnetron Titan'), ('magnetronAu', 'Magnetron Gold'), ('snowball', 'Snowball'), ('toffy', 'Toffy')], default='magnetronTi', max_length=20, null=True)),
                ('comment', models.TextField(blank=True)),
                ('nid_file', models.FileField(blank=True, upload_to='nanoparticles')),
                ('spectroscopy', models.BooleanField(default=False)),
                ('conductivity', models.BooleanField(default=False)),
                ('xps', models.BooleanField(default=False)),
                ('image_size', models.FloatField(blank=True, null=True, verbose_name='Image Size in µm')),
                ('coating', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nanoparticles.coating')),
            ],
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Substrate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=500)),
                ('width', models.FloatField(blank=True, null=True, verbose_name='Width (mm)')),
                ('height', models.FloatField(blank=True, null=True, verbose_name='Height (mm)')),
                ('thickness', models.FloatField(blank=True, null=True, verbose_name='Thickness (mm)')),
            ],
        ),
        migrations.CreateModel(
            name='MeasurementData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forward_phase_data', models.BinaryField()),
                ('forward_amplitude_data', models.BinaryField()),
                ('forward_z_axis_data', models.BinaryField()),
                ('backward_phase_data', models.BinaryField()),
                ('backward_amplitude_data', models.BinaryField()),
                ('backward_z_axis_data', models.BinaryField()),
                ('forward_phase_image', models.ImageField(upload_to='nanoparticles')),
                ('forward_amplitude_image', models.ImageField(upload_to='nanoparticles')),
                ('forward_z_axis_image', models.ImageField(upload_to='nanoparticles')),
                ('backward_phase_image', models.ImageField(upload_to='nanoparticles')),
                ('backward_amplitude_image', models.ImageField(upload_to='nanoparticles')),
                ('backward_z_axis_image', models.ImageField(upload_to='nanoparticles')),
                ('measurement', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='nanoparticles.measurement')),
            ],
        ),
        migrations.AddField(
            model_name='measurement',
            name='substrate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='nanoparticles.substrate'),
        ),
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=500)),
                ('image1', models.ImageField(blank=True, null=True, upload_to='journal/journalImage/')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='journal/journalImage/')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='journal/journalImage/')),
                ('image4', models.ImageField(blank=True, null=True, upload_to='journal/journalImage/')),
                ('image5', models.ImageField(blank=True, null=True, upload_to='journal/journalImage/')),
                ('file', models.FileField(blank=True, null=True, upload_to='journal/journalFiles/', verbose_name='File which can be downloaded')),
                ('comment', ckeditor.fields.RichTextField(blank=True)),
                ('measurement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='nanoparticles.measurement')),
                ('operator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='nanoparticles.operator')),
            ],
            options={
                'ordering': ('-id',),
                'abstract': False,
            },
        ),
    ]