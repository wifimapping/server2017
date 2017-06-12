# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingestion', '0002_auto_20150411_1212'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='wifiscan',
            options={'managed': False},
        ),
    ]
