# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cheminventory', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gascylinder',
            name='last_user',
            field=models.ForeignKey(default=1, to='cheminventory.Person'),
            preserve_default=False,
        ),
    ]
