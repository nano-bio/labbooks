# Generated by Django 3.2.9 on 2021-11-09 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('toffy', '0005_journalentry'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='journalentry',
            options={'ordering': ('-id',)},
        ),
    ]
