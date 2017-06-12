# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingestion', '0006_auto_20160602_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='uniquelocations',
            name='idx',
            field=models.AutoField(serialize=False, primary_key=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='uniquelocations',
            name='lat',
            field=models.DecimalField(max_digits=8, decimal_places=4),
        ),
        migrations.AlterField(
            model_name='uniquelocations',
            name='lng',
            field=models.DecimalField(max_digits=8, decimal_places=4),
        ),
        migrations.AlterUniqueTogether(
            name='uniquelocations',
            unique_together=set([('lat', 'lng')]),
        ),
    ]
