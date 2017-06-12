# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingestion', '0005_auto_20160602_1412'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='uniquelocations',
            options={'managed': True},
        ),
    ]
