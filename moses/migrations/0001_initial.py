# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-03-19 13:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, upload_to=b'moses')),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('short_description', models.CharField(max_length=200)),
                ('step_size', models.IntegerField(help_text=b'Unit: micro meter')),
                ('x_min', models.IntegerField(blank=True, help_text=b'Unit: micro meter', null=True)),
                ('x_max', models.IntegerField(blank=True, help_text=b'Unit: micro meter', null=True)),
                ('y_min', models.IntegerField(blank=True, help_text=b'Unit: micro meter', null=True)),
                ('y_max', models.IntegerField(blank=True, help_text=b'Unit: micro meter', null=True)),
                ('evaluation_file', models.ManyToManyField(blank=True, help_text=b'Zip evaluation files', related_name='evaluation_file', to='moses.File')),
                ('image', models.ManyToManyField(blank=True, related_name='image', to='moses.File', verbose_name=b'Evaluated Image')),
            ],
        ),
        migrations.CreateModel(
            name='Target',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('comment', models.TextField(blank=True, max_length=1000)),
                ('files', models.ManyToManyField(blank=True, related_name='target_image', to='moses.File')),
            ],
        ),
        migrations.AddField(
            model_name='measurement',
            name='target',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='moses.Target'),
        ),
    ]