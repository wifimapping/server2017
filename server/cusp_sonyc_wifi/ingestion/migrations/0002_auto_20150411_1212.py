# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingestion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WifiScan',
            fields=[
                ('idx', models.BigIntegerField(serialize=False, primary_key=True)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('acc', models.FloatField()),
                ('altitude', models.FloatField()),
                ('time', models.DecimalField(max_digits=15, decimal_places=0)),
                ('device_mac', models.CharField(max_length=20)),
                ('app_version', models.CharField(max_length=10)),
                ('droid_version', models.CharField(max_length=10)),
                ('device_model', models.CharField(max_length=50)),
                ('ssid', models.CharField(max_length=100)),
                ('bssid', models.CharField(max_length=20)),
                ('caps', models.CharField(max_length=100)),
                ('level', models.FloatField()),
                ('freq', models.FloatField()),
            ],
            options={
                'db_table': 'wifi_scan',
            },
        ),
        migrations.DeleteModel(
            name='Scan',
        ),
    ]
