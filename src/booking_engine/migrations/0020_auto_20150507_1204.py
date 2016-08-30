# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booking_engine', '0019_remove_booking_engine_pricesheet_unit_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking_engine_payment_plan',
            name='as_of_date',
            field=models.DateField(max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='booking_engine_payment_plan',
            name='is_active',
            field=models.BooleanField(),
            preserve_default=True,
        ),
    ]
