# Generated by Django 3.2.9 on 2021-11-09 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('clustof', '0005_rename_attachment_journalentry_file'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='journalentry',
            options={'ordering': ('-id',)},
        ),
    ]
