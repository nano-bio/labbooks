# Generated by Django 3.2.12 on 2022-08-02 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nanoparticles', '0005_transfer_sputter_method'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='measurement',
            name='sputter_method',
        ),
    ]