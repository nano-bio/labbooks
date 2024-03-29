# Generated by Django 3.2.12 on 2022-08-01 13:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('nanoparticles', '0003_alter_measurement_sputter_method'),
    ]

    operations = [
        migrations.CreateModel(
            name='SputterMethod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='measurement',
            name='sputter_method_link',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='nanoparticles.sputtermethod'),
        ),
    ]
