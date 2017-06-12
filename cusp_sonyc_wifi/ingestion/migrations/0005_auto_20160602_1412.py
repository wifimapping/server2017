# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingestion', '0004_uniquelocations'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='uniquelocations',
            options={'managed': False},
        ),
    ]
