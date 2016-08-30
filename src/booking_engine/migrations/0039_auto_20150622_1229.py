# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0038_auto_20150622_1223'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking_engine_units',
            name='Availability',
        ),
        migrations.RemoveField(
            model_name='booking_engine_units',
            name='builtup_area',
        ),
        migrations.RemoveField(
            model_name='booking_engine_units',
            name='carpet_area',
        ),
        migrations.RemoveField(
            model_name='booking_engine_units',
            name='door_number',
        ),
        migrations.RemoveField(
            model_name='booking_engine_units',
            name='floor_number',
        ),
        migrations.RemoveField(
            model_name='booking_engine_units',
            name='price_per_sqft',
        ),
        migrations.RemoveField(
            model_name='booking_engine_units',
            name='super_builtup_area',
        ),
        migrations.RemoveField(
            model_name='booking_engine_units',
            name='tower_id',
        ),
    ]
