# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0040_booking_engine_units_unit_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_engine_payment_plan',
            name='is_default',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='booking_engine_project_pricesheet',
            name='is_default',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
