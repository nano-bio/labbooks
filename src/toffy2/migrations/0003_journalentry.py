# Generated by Django 3.2.7 on 2021-09-10 07:30

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('toffy2', '0002_auto_20200916_1637'),
    ]

    operations = [
        migrations.CreateModel(
            name='JournalEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('title', models.CharField(max_length=500)),
                ('image1', models.ImageField(blank=True, null=True, upload_to='journal/journalImage/')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='journal/journalImage/')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='journal/journalImage/')),
                ('image4', models.ImageField(blank=True, null=True, upload_to='journal/journalImage/')),
                ('image5', models.ImageField(blank=True, null=True, upload_to='journal/journalImage/')),
                ('file', models.FileField(blank=True, null=True, upload_to='journal/journalFiles/', verbose_name='File which can be downloaded')),
                ('comment', ckeditor.fields.RichTextField(blank=True)),
                ('measurement', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='toffy2.measurement')),
                ('operator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='toffy2.operator')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]