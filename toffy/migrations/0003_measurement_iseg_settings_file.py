# Generated by Django 3.0.8 on 2020-07-13 08:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toffy', '0002_auto_20200703_1603'),
    ]

    operations = [
        migrations.AddField(
            model_name='measurement',
            name='iseg_settings_file',
            field=models.FileField(blank=True, upload_to='toffy/isegFiles/'),
        ),
    ]
