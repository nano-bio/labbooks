# Generated by Django 3.2.9 on 2021-12-07 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labinventory', '0002_auto_20211207_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='mobile',
            field=models.IntegerField(blank=True, help_text='Use numbers only, i.e. 0043699123456789', null=True),
        ),
    ]
