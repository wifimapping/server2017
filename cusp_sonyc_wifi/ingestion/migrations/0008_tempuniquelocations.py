# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingestion', '0007_auto_20160602_1426'),
    ]

    operations = [
        migrations.CreateModel(
            name='TempUniqueLocations',
            fields=[
                ('idx', models.AutoField(serialize=False, primary_key=True)),
                ('lat', models.DecimalField(max_digits=8, decimal_places=4)),
                ('lng', models.DecimalField(max_digits=8, decimal_places=4)),
            ],
            options={
                'db_table': 'temp_unique_locations',
                'managed': True,
            },
        ),
    ]
