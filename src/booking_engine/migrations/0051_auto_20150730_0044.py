# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0050_auto_20150729_1936'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_engine_pricesheet',
            name='broker_id',
            field=models.CharField(default=0, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking_engine_pricesheet',
            name='project_type_id',
            field=models.CharField(default=0, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking_engine_pricesheet',
            name='tower_id',
            field=models.CharField(default=0, max_length=50, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking_engine_pricesheet',
            name='unit_variant_id',
            field=models.CharField(default=0, max_length=50, null=True),
            preserve_default=True,
        ),
    ]
