# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingestion', '0003_auto_20150411_1213'),
    ]

    operations = [
        migrations.CreateModel(
            name='UniqueLocations',
            fields=[
                ('lat', models.FloatField(serialize=False)),
                ('lng', models.FloatField(primary_key=True)),
            ],
            options={
                'db_table': 'unique_locations',
                'managed': True,
            },
        ),
    ]
