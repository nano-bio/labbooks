# Generated by Django 3.0.8 on 2020-07-03 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snowball', '0001_squashed_0009_auto_20180312_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journalentry',
            name='attachment',
            field=models.FileField(blank=True, default='', upload_to='snowball/techjournal/'),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='operator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='snowball.Operator'),
        ),
        migrations.AlterField(
            model_name='journalentry',
            name='written_notes',
            field=models.ImageField(blank=True, upload_to='snowball/techjournal/notes/'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='chan',
            field=models.FloatField(default=3500.0, verbose_name='Channeltron Voltage'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='datafile',
            field=models.FileField(max_length=400, upload_to='snowball/%Y/%m/%d/%H/%M/%S/'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='ec',
            field=models.FloatField(default=100.0, verbose_name='Electron Current'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='ec_2',
            field=models.FloatField(default=100.0, verbose_name='Electron Current IS2'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='ee',
            field=models.FloatField(default=70.0, verbose_name='Electron Energy'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='ee_2',
            field=models.FloatField(default=70.0, verbose_name='Electron Energy IS2'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='he_pres',
            field=models.FloatField(default=20.0, verbose_name='He pressure'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='he_temp',
            field=models.FloatField(default=9.5, verbose_name='He temp'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='operator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='snowball.Operator'),
        ),
        migrations.AlterField(
            model_name='measurement',
            name='text',
            field=models.TextField(blank=True, max_length=1500, verbose_name='Comment'),
        ),
        migrations.AlterField(
            model_name='turbopumpstatus',
            name='pump',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='snowball.Turbopump'),
        ),
    ]
