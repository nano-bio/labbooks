# Generated by Django 3.2.12 on 2022-08-01 13:31

from django.db import migrations


def link_designation(apps, schema_editor):
    Measurement = apps.get_model('nanoparticles', 'Measurement')
    SputterMethod = apps.get_model('nanoparticles', 'SputterMethod')
    for measurement in Measurement.objects.all():
        if measurement.sputter_method:
            sputter_method, created = SputterMethod.objects.get_or_create(name=measurement.get_sputter_method_display())
            measurement.sputter_method_link = sputter_method
            measurement.save()


class Migration(migrations.Migration):
    dependencies = [
        ('nanoparticles', '0004_auto_20220801_1529'),
    ]

    operations = [
        migrations.RunPython(link_designation),
    ]