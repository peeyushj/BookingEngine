# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0052_booking_engine_units_total_sale_value'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_engine_units',
            name='project_type_id',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking_engine_units',
            name='tower_id',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking_engine_units',
            name='unit_variant_id',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
    ]
