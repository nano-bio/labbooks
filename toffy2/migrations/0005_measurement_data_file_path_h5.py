# Generated by Django 3.2.12 on 2022-06-13 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toffy2', '0004_alter_journalentry_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='data_file_path_h5',
            field=models.CharField(blank=True, default='Z:\\Experiments\\Toffy2\\Measurements\\RAW-TOFWERK-Data\\', help_text="The path must start with Z:\\, otherwise spectra viewer won't work!", max_length=150),
        ),
    ]
